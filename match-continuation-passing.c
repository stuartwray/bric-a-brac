#include <stdio.h>
#include <stdlib.h>

#include "scw-misc.h"

/* 
   Originally copied from "A regular expression matcher" by
   Brian Kernighan (Ch 1 of "Beautiful Code").
   ... then transformed into continuation-passing style using the 
   technique in "The Role of the Study of Programming Languages in
   the Education of a Programmer" by Daniel P. Friedman
   (Although it might seem bizzare, I found it easiest to do this by 
   translating the original C into Python, transforming *that* into
   continuation-passing style, then translating the result back to C.)
*/

#define STACK_IS_EMPTY(_top, _base) ((_top) == (&(_base)[0]))
#define PUSH(_top, _v) *((_top)++) = ((int) (_v))
#define POP(_top) (*(--(_top))) 

#define CONT1 0
#define CONT2 1

int match(char *_regexp, char *_text)
{
  /* "registers" */
  char *regexp = NULL;
  char *text = NULL;
  int stackarray[100]; /* more than enough for toy examples */
  int *stack =  &stackarray[0];
  int value = 0;
  char ch = '\0';
  int label;

  /* set up registers */
  regexp = _regexp;
  text   = _text;
  goto match1;

 match1:
  /* search for regexp anywhere in text */
  if (regexp[0] == '^') {
    regexp = regexp + 1;
    goto matchhere;
  } else {
    goto matchanywhere;
  }

 matchanywhere:
  PUSH(stack, text);
  PUSH(stack, regexp);
  PUSH(stack, CONT1);
  goto matchhere;

 matchhere:
  /* search for regexp at start of text */
  if (regexp[0] == '\0') {
    value = 1;
    goto apply_cont;
  }
  if (regexp[1] == '*') {
    ch     = regexp[0];
    regexp = regexp + 2;
    goto matchstar;
  }
  if (regexp[0] == '$' && regexp[1] == '\0') {
    value = (*text == '\0');
    goto apply_cont;
  }
  if (*text != '\0' && (regexp[0] == '.' || regexp[0] == *text)) {
    regexp = regexp + 1;
    text   = text + 1;
    goto matchhere;
  }
  value = 0;
  goto apply_cont;

 matchstar:
  /* search for ch* at start of text, followed by regexp */
  PUSH(stack, text);
  PUSH(stack, regexp);
  PUSH(stack, ch);
  PUSH(stack, CONT2);
  goto matchhere;

 apply_cont:
  if (STACK_IS_EMPTY(stack, stackarray)) {
    return value;
  }
  label = POP(stack);
  if (label == CONT1) {
    regexp = (char *) POP(stack);
    text   = (char *) POP(stack);
    if (value) {
      goto apply_cont;
    }
    if (*text == '\0') {
      value = 0;
      goto apply_cont;
    }
    text = text + 1;
    goto matchanywhere;
  } else {
    /* Here, label == CONT2 */
    ch     = (char)   POP(stack);
    regexp = (char *) POP(stack);
    text   = (char *) POP(stack);
    if (value) {
      goto apply_cont;
    }
    if (*text == '\0') {
      value = 0;
      goto apply_cont;
    }
    if (!(*text == ch || ch == '.')) {
      value = 0;
      goto apply_cont;
    }
    text = text + 1;
    goto matchstar;
  }
}

int main(int argc, char **argv)
{
  printf("Testing match functions (continuation-passing style)\n");
  ASSERT(match("", ""));
  ASSERT(match("$", ""));
  ASSERT(match("c", "c"));
  ASSERT(match("c", "cccccc"));
  ASSERT(match("c", "aaaaac"));
  ASSERT(match("c", "aacaaa"));
  ASSERT(match("^c", "caaaa"));
  ASSERT(!match("^c", "aacaa"));
  ASSERT(match("c$", "aaaac"));
  ASSERT(!match("c$", "aacaa"));
  ASSERT(match("^a.*a$", "a banana a"));       
  ASSERT(match("^a.*a.*a$", "a banana a"));
  ASSERT(match("^a.*.*a$", "a banana a"));    
  ASSERT(match("b.*.*a$", "a banana a"));
  ASSERT(!match("a*b", "a"));
  ASSERT(match("a*b", "b"));
  ASSERT(match("a*b", "ab"));
  ASSERT(match("a*b", "aaaaaaab"));
  ASSERT(match("a*b", "cccccaaaaaaab"));
  ASSERT(match("a*", ""));
  ASSERT(match("a*", "b"));
  printf("Finished ok\n");
  return 0;
}
