#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error\n");
        return 1;
    }

    string arg = argv[1];
    int n = atoi(arg);

    if (n % 2 != 1)
    {
        printf("Error\n");
        return 2;
    }

    int spaces = n / 2;

    for (int i = 1; i <= n; i += 2)
    {
        for (int j = 0; j < spaces; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }
        printf("\n");
        spaces--;
    }
    spaces++;
    for (int i = n - 2; i >= 1; i -= 2)
    {
        spaces++;
        for (int j = 0; j < spaces; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }
        printf("\n");
    }


    return 0;
}