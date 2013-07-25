#include <stdio.h>
#include <stdlib.h>

#include "scw-misc.h"

/* 
   This is more-or-less copied from "A regular expression matcher" by 
   Brian Kernighan (Ch 1 of "Beautiful Code").
*/

/* prototypes for mutually recursive functions */
int matchhere(char *regexp, char *text);
int matchstar(char ch, char *regexp, char *text);

int match(char *regexp, char *text)
/* search for regexp anywhere in text */
{
  if (regexp[0] == '^')
    return matchhere(regexp + 1, text);
  do { /* need to check even if text is empty */
    if (matchhere(regexp, text))
      return 1;
  } while (*text++ != '\0');
  return 0;
}
   
int matchhere(char *regexp, char *text)
/* search for regexp at start of text */
{
  if (regexp[0] == '\0')
    return 1;
  if (regexp[1] == '*')
      return matchstar(regexp[0], regexp+2, text);
  if (regexp[0] == '$' && regexp[1] == '\0')
    return *text == '\0';
  if (*text != '\0' && (regexp[0] == '.' || regexp[0] == *text))
    return matchhere(regexp+1, text+1);
  return 0;
}

int matchstar(char ch, char *regexp, char *text)
/* search for ch* at start of text, followed by regexp */
{
  do {
    if (matchhere(regexp, text))
      return 1;
  } while (*text != '\0' && (*text++ == ch || ch == '.'));
  return 0;
}    
      
int main(int argc, char **argv)
{
  printf("Testing match functions\n");
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
