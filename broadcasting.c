#include <stdio.h>

#define ROWS 3
#define COLS 3

void broadcast_and_add(int A[ROWS][COLS], int B[COLS], int result[ROWS][COLS]) {
	int i, j;
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            // B dizisini her satýra 'broadcast' ediyoruz
            result[i][j] = A[i][j] + B[j];
        }
    }
    printf("%d\n", ROWS);
}

int main() {
	int i, j;
    int A[ROWS][COLS] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    int B[COLS] = {10, 20, 30};

    int result[ROWS][COLS];

    broadcast_and_add(A, B, result);

    // Sonucu yazdýralým
    printf("Resultant Matrix:\n");
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            printf("%d ", result[i][j]);
        }
        printf("\n");
    }

    return 0;
}

