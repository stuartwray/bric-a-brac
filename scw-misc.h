/*
    Miscellaneous debugging helper functions/macros etc
*/

#ifndef _SCW_MISC_
#define _SCW_MISC_

/* ---------------------------------------------------------------------- 
 * ASSERT
 *
 */

#undef ASSERT
#undef TRACE

#ifndef NDEBUG

static void  _AssertFailure(const char * pszFile, unsigned uLine)
{
    printf("%s:%d: +++ ASSERT FAILURE\n", pszFile, uLine);   
    exit(1);
}

#define ASSERT(_cond) \
        if (_cond) \
            { } \
        else \
             _AssertFailure(__FILE__, __LINE__)

#define TRACE(_fmt,_args...) \
        printf("TRACE: " _fmt , ## _args)

#else

#define ASSERT(_cond)  { }
#define TRACE(_fmt,_args...) { }

#endif /* NDEBUG */

/* ---------------------------------------------------------------------- 
 * Misc declarations
 *
 */

/* should really be using stdint.h */
typedef unsigned char U8;
typedef unsigned int  U32;

/* should really be using stdbool.h */
typedef _Bool         BOOL;
#define FALSE  0
#define TRUE   1

#endif /* _SCW_MISC_ */
