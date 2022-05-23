#include <stdio.h>
#include <stdlib.h>

#define LENGTH 16

// length is fixed at 16
int* euclid1(int hits, int offset)
{
    static int r[LENGTH];
    int s1, s2, s3, s4;

    for (int i=0; i < LENGTH; i++) {
        s1 = i + offset;
        s2 = s1 * hits;
        s3 = s2 % LENGTH;
        s4 = s3 < hits;
        r[i] = s4;

    }
    return r;
}


int test_euclid1(void)
{
    int *p;

    p = euclid1(4, 0);

    for (int i=0; i < LENGTH; i++) {
        printf( "*(p + %d) : %d\n", i, *(p + i));
    }
    return 0;
}

// length is dynamically set
int* euclid2(int hits, int length, int offset)
{
    int *r = calloc(length, sizeof(int));
    if (r == NULL) {
        printf("Unable to allocate memory.\n");
        exit(-1);
    }

    int s1, s2, s3, s4;

    for (int i=0; i < length; i++) {
        s1 = i + offset;
        s2 = s1 * hits;
        s3 = s2 % length;
        s4 = s3 < hits;
        r[i] = s4;

    }
    return r;
}

int test_euclid2(void)
{
    int *p;

    p = euclid2(4, 16, 0);

    for (int i=0; i < 16; i++) {
        printf( "*(p + %d) : %d\n", i, *(p + i));
    }

    free(p);

    return 0;
}

// length is dynamically set
int euclid3(int hits, int length, int offset, int* arr)
{
    int s1, s2, s3, s4;

    for (int i=0; i < length; i++) {
        s1 = i + offset;
        s2 = s1 * hits;
        s3 = s2 % length;
        s4 = s3 < hits;
        arr[i] = s4;

    }
    return 0;
}

int test_euclid3(void)
{
    int length = 16;

    int *p = calloc(length, sizeof(int));
    if (p == NULL) {
        printf("Unable to allocate memory.\n");
        exit(-1);
    }

    euclid3(4, length, 0, p);

    for (int i=0; i < length; i++) {
        printf( "*(p + %d) : %d\n", i, *(p + i));
    }

    free(p);

    return 0;
}


int main()
{
    test_euclid1();
    printf("\n");
    test_euclid2();
    printf("\n");
    test_euclid3();

    return 0;
}