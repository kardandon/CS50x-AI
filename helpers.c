#include "helpers.h"
#include <stdlib.h>
#include <math.h>
#include <cs50.h>

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int rounded;
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            rounded = round(((float)image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3);
            image[i][j].rgbtRed = rounded;
            image[i][j].rgbtBlue = rounded;
            image[i][j].rgbtGreen = rounded;
        }
    }
    return;
}

void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int originalRed;
    int originalBlue;
    int originalGreen;
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            originalRed = image[i][j].rgbtRed;
            originalBlue = image[i][j].rgbtBlue;
            originalGreen = image[i][j].rgbtGreen;
            image[i][j].rgbtRed = round( 0.393 * originalRed + 0.769 * originalBlue + 0.189 * originalGreen) <= 255 ? round( 0.393 * originalRed + 0.769 * originalBlue + 0.189 * originalGreen) : 255;
            image[i][j].rgbtBlue = round(0.349 * originalRed + 0.686 * originalBlue + 0.168 * originalGreen) <= 255 ? round(0.349 * originalRed + 0.686 * originalBlue + 0.168 * originalGreen) : 255;
            image[i][j].rgbtGreen = round(0.272 * originalRed + 0.534 * originalBlue + 0.131 * originalGreen) <= 255 ? round(0.272 * originalRed + 0.534 * originalBlue + 0.131 * originalGreen) : 255;
        }
    }
    return;
}

void swap (RGBTRIPLE *a, RGBTRIPLE *b){
    RGBTRIPLE tmp;
    tmp.rgbtRed = a->rgbtRed;
    tmp.rgbtBlue = a->rgbtBlue;
    tmp.rgbtGreen = a->rgbtGreen;
    a->rgbtRed = b->rgbtRed;
    a->rgbtBlue = b->rgbtBlue;
    a->rgbtGreen = b->rgbtGreen;
    b->rgbtRed = tmp.rgbtRed;
    b->rgbtBlue = tmp.rgbtBlue;
    b->rgbtGreen = tmp.rgbtGreen;
    return;
}
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width/2 ; j++)
        {
            swap(&image[i][j], &image[i][width-1-j]);
        }
    }
    return;
}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    float tempRed;
    float tempBlue;
    float tempGreen;
    int count;
    RGBTRIPLE orig[height][width];
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            orig[i][j].rgbtRed = image[i][j].rgbtRed;
            orig[i][j].rgbtBlue = image[i][j].rgbtBlue;
            orig[i][j].rgbtGreen = image[i][j].rgbtGreen;
        }
    }
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            tempRed = 0;
            tempBlue = 0;
            tempGreen = 0;
            count = 0;
            for (int k = -1 ; k < 2 ; k++)
            {
                for (int z = -1 ; z < 2 ; z++)
                {
                    if (i + k >= 0 && i + k < height && j + z >= 0 && j + z < width)
                    {
                        tempRed += orig[i + k][j + z].rgbtRed;
                        tempGreen += orig[i + k][j + z].rgbtGreen;
                        tempBlue += orig[i + k][j + z].rgbtBlue;
                        count++;
                    }
                }
            }
            image[i][j].rgbtRed = (int)round(tempRed/count);
            image[i][j].rgbtGreen = (int)round(tempGreen/count);
            image[i][j].rgbtBlue = (int)round(tempBlue/count);
        }
    }
    return;
}
