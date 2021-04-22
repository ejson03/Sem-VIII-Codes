#include <stdio.h>
int max1(int a, int b)
{
    if (a > b)
        return a;
    else
        return b;
}
  
void display(int e1, int e2,
             int p1[5], int p2[3])
{
    int i;
  
    printf("\nThe time stamps of "
           "events in P1:\n");
  
    for (i = 0; i < e1; i++) {
        printf("%d ", p1[i]);
    }
  
    printf("\nThe time stamps of "
           "events in P2:\n");
  
    // Print the array p2[]
    for (i = 0; i < e2; i++)
        printf("%d ", p2[i]);
}
void lamportLogicalClock(int e1, int e2,
                         int m[5][3])
{
    int i, j, k, p1[e1], p2[e2];
    for (i = 0; i < e1; i++)
        p1[i] = i + 1;
  
    for (i = 0; i < e2; i++)
        p2[i] = i + 1;
  
    for (i = 0; i < e2; i++)
        printf("\te2%d", i + 1);
  
    for (i = 0; i < e1; i++) {
  
        printf("\n e1%d \t", i + 1);
  
        for (j = 0; j < e2; j++)
            printf("%d\t", m[i][j]);
    }
  
    for (i = 0; i < e1; i++) {
        for (j = 0; j < e2; j++) {
  
            // Change the timestamp if the
            // message is sent
            if (m[i][j] == 1) {
                p2[j] = max1(p2[j], p1[i] + 1);
                for (k = j + 1; k < e2; k++)
                    p2[k] = p2[k - 1] + 1;
            }
  
            // Change the timestamp if the
            // message is reeived
            if (m[i][j] == -1) {
                p1[i] = max1(p1[i], p2[j] + 1);
                for (k = i + 1; k < e1; k++)
                    p1[k] = p1[k - 1] + 1;
            }
        }
    }
  
    // Function Call
    display(e1, e2, p1, p2);
}
  
// Driver Code
int main()
{
    int e1 = 5, e2 = 3, m[5][3];
    m[0][0] = 0;
    m[0][1] = 0;
    m[0][2] = 0;
    m[1][0] = 0;
    m[1][1] = 0;
    m[1][2] = 1;
    m[2][0] = 0;
    m[2][1] = 0;
    m[2][2] = 0;
    m[3][0] = 0;
    m[3][1] = 0;
    m[3][2] = 0;
    m[4][0] = 0;
    m[4][1] = -1;
    m[4][2] = 0;
    lamportLogicalClock(e1, e2, m);
  
    return 0;
}
/*
Output 
e21     e22     e23
 e11    0       0       0       
 e12    0       0       1       
 e13    0       0       0       
 e14    0       0       0       
 e15    0       -1      0       
The time stamps of events in P1:
1 2 3 4 5
The time stamps of events in P2:
1 2 3
*/