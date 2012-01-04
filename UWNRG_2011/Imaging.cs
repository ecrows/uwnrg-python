using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;
using System.Drawing.Imaging;
using System.Threading;
//using System.Windows.Forms;
namespace UWNRG_2011
{
    unsafe class Imaging
    {
        static char[,] data;
        TIS.Imaging.ICImagingControl ic;
        const int hori_threshold = 125;
        const int vert_threshold = 190;
        const int comp_threshold = 5;
        const int non_comp_threshold = 3;
        static int grid_h = 32;
        static int grid_w = 32;

        /// <summary>
        /// Constructor
        /// </summary>
        public Imaging(TIS.Imaging.ICImagingControl icImagingControl)
        {
            ic = icImagingControl;
        }

        /// <summary>
        /// Captures and returns an image from the Imaging Device.
        /// </summary>
        /// <returns>A Bitmap storing the image captured from the camera.</returns>
        public Bitmap Capture()
        {
            if (ic.DeviceValid)
            {
                ic.MemorySnapImage();
                TIS.Imaging.ImageBuffer buffer;
                buffer = ic.ImageActiveBuffer;
                return buffer.Bitmap;                
            }
            return null;
        }
        /// <summary>
        /// Processes a given Bitmap to return a 2D char array of size [grid_width,grid_height]
        /// </summary>
        /// <param name="image">A Bitmap representing the field to be processed</param>
        /// <param name="grid_width">The width of the virtual grid</param>
        /// <param name="grid_height">The height of the virtual grid</param>
        /// <param name="comp_camera">States whether the camera being used is the competition one or not. The competition camera will have a slightly higher threshold</param>
        /// <returns>A 2D char array with an 'x' where there is a wall, and a 'o' where there is no wall detected</returns>
        public char[,] Process(Bitmap image, int grid_width, int grid_height, Boolean comp_camera)
        {
            grid_h = grid_height;
            grid_w = grid_width;
            data = new char[grid_width, grid_height];
            int width = 2;
            Bitmap swap = (Bitmap)image.Clone();
            //***********************************
            //Set up some pointers to access the images. Pointers are a necessary evil in this case, to speed up image processing
            BitmapData image_data = image.LockBits(new Rectangle(0, 0, image.Width, image.Height), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
            BitmapData swap_data = swap.LockBits(new Rectangle(0, 0, image.Width, image.Height), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
            Byte* image_start = (Byte*)image_data.Scan0.ToPointer();
            int image_stride = image_data.Stride;
            Byte* swap_start = (Byte*)swap_data.Scan0.ToPointer();
            int swap_stride = swap_data.Stride;
            //***********************************

            Median_Filter(image.Width, image.Height, width, image_start, image_stride, swap_start, swap_stride);

            Swap(ref image_start, ref swap_start);
            if (comp_camera)
            {
                Adaptive_Threshold(image.Width, image.Height, width, image_start, image_stride, swap_start, swap_stride,comp_threshold);
            }
            else
            {
                Adaptive_Threshold(image.Width, image.Height, width, image_start, image_stride, swap_start, swap_stride, non_comp_threshold);
            }
            Swap(ref image_start, ref swap_start);
            int size = 800;
            int[,] accumulator = new int[180, size * 2];
            Accumulate(image.Width, image.Height, width, image_start, image_stride, size, accumulator);

            int theta_avg_vert = 0;
            int theta_avg_hori = 0;
            Find_Edges(size, accumulator, ref theta_avg_vert, ref theta_avg_hori);
            theta_avg_vert = (theta_avg_vert + 180) % 180;
            int x;
            int y;
            int max_dist = 0;
            int count_max = 0;
            int max_vert = 0;
            int min_vert = 0;
            int max_hori = 0;
            int min_hori = 0;
            //Find the vertical line with a certain number of feature pixels that is closest to the center of the image,
            //except finds the line that is at the bottom of the rectangle
            for (y = image.Height / 2; y < image.Height - width; y++)
            {
                if (accumulator[theta_avg_hori, y + size] > count_max)
                {
                    max_dist = y;
                    count_max = accumulator[theta_avg_hori, y + size];
                }
                if (accumulator[theta_avg_hori, y + size] > hori_threshold)
                {
                    max_dist = y;
                    break;
                }
            }
            max_hori = max_dist;
            count_max = 0;
           //Find the vertical line with a certain number of feature pixels that is closest to the center of the image,
            //except finds the line that is at the top of the rectangle
            for (y = image.Height / 2; y > width; y--)
            {
                if (accumulator[theta_avg_hori, y + size] > count_max)
                {
                    max_dist = y;
                    count_max = accumulator[theta_avg_hori, y + size];
                }
                if (accumulator[theta_avg_hori, y + size] > hori_threshold)
                {
                    max_dist = y;
                    break;
                }
            }
            //Find the horizontal line with a certain number of feature pixels that is closest to the center of the image,
            //except finds the line that is at the right of the rectangle
            min_hori = max_dist;
            count_max = 0;
            for (x = image.Width / 2; x < image.Width - width - 1; x++)
            {
                if (accumulator[theta_avg_vert, x + size] > count_max)
                {
                    max_dist = x;
                    count_max = accumulator[theta_avg_vert, x + size];
                }
                if (accumulator[theta_avg_vert, x + size] > vert_threshold)
                {
                    max_dist = x;
                    break;
                }
                if (accumulator[theta_avg_vert, -x + size] > count_max)
                {
                    max_dist = x;
                    count_max = accumulator[theta_avg_vert, -x + size];
                }
                if (accumulator[theta_avg_vert, -x + size] > vert_threshold)
                {
                    max_dist = x;
                    break;
                }

            }
            //Find the horizontal line with a certain number of feature pixels that is closest to the center of the image,
            //except finds the line that is at the left of the rectangle
            max_vert = max_dist;
            count_max = 0;
            for (x = image.Width / 2; x > width; x--)
            {
                if (accumulator[theta_avg_vert, x + size] > count_max)
                {
                    max_dist = x;
                    count_max = accumulator[theta_avg_vert, x + size];
                }
                if (accumulator[theta_avg_vert, x + size] > 190)
                {
                    max_dist = x;
                    break;
                }
                if (accumulator[theta_avg_vert, -x + size] > count_max)
                {
                    max_dist = x;
                    count_max = accumulator[theta_avg_vert, -x + size];
                }
                if (accumulator[theta_avg_vert, -x + size] > 190)
                {
                    max_dist = x;
                    break;
                }

            }
            min_vert = max_dist;
            max_vert += 7;
            min_vert -= 10;
            max_hori += 10;
            min_hori -= 7;
            min_vert = Math.Max(min_vert, width);
            max_vert = Math.Min(max_vert, image.Width - width);
            max_hori = Math.Min(max_hori, image.Height - width);
            min_hori = Math.Max(min_hori, width);
            //Forces those lines that have angles above 135 to have negative angles. Simplifies calculations later on
            if (theta_avg_vert > 135)
            {
                theta_avg_vert = theta_avg_vert - 180;
            }
            double d_theta_hori = theta_avg_hori * Math.PI / 180;
            double d_theta_vert = theta_avg_vert * Math.PI / 180;
            int[,] grid = new int[grid_width, grid_height];
            //Counts the number of pixels that fall within each grid position. Accounts for orientation of the grid.
            for (x = min_vert; x < max_vert; x++)
            {
                int temp_min = (int)((min_hori - x * Math.Cos(d_theta_hori)) / Math.Sin(d_theta_hori));
                int temp_max = temp_min + max_hori - min_hori;
                for (y = temp_min; y < Math.Min(temp_max, image.Height); y++)
                {
                    int x_pos = (int)((x - Math.Sin(d_theta_vert) * y) / Math.Cos(d_theta_vert));
                    //Checks to make sure a pixel has been marked as a feature pixel
                    if (*(image_start + image_stride * y + x_pos * 4) == 255)
                    {
                        int temp_x = (int)((min_vert - Math.Sin(d_theta_vert) * y) / Math.Cos(d_theta_vert));
                        x_pos = (int)((x_pos - temp_x) / (double)(max_vert - min_vert) * (grid_width - 1));
                        int y_pos = (int)((temp_max - y) / (double)(temp_max - temp_min) * (grid_height - 1));
                        if (x_pos < 32 && x_pos >= 0 && y_pos < 32 && y_pos >= 0)
                        {
                            grid[x_pos, y_pos]++;
                        }
                    }
                }
            }
            //Calculate threshold based on number of pixels in each grid square. Threshold is 1%.
            int threshold = (int)((max_vert - min_vert) * (max_hori - min_hori) / (double)(grid_height * grid_width) / 100.0);
            for (int t = 0; t < grid_height; t++)
            {
                for (int i = 0; i < grid_width; i++)
                {
                    data[i, t] = grid[i, t] > threshold ? 'x' : '.';
                }
                data[grid_width - 1, t] = 'x';
            }
            for (int i = 0; i < grid_width; i++)
            {
                data[i, grid_height - 1] = 'x';
            }


            image.UnlockBits(image_data);
            swap.UnlockBits(swap_data);
            return data;
        }
        /// <summary>
        /// Finds the robot's position based on an estimate and a distance maximum
        /// </summary>
        /// <param name="x_guess">The robot's last known x coordinate</param>
        /// <param name="y_guess">The robot's last known y coordinate</param>
        /// <param name="distance">The estimated distance the robot should be within</param>
        public Point Find_Robot(int x_guess, int y_guess, int distance)
        {
            double min_dist = Math.Sqrt(grid_h * grid_h + grid_w * grid_w);
            double temp_dist = 0;
            Point position = new Point(x_guess, y_guess);
            
                for (int x = Math.Max(0,x_guess - distance); x < Math.Min(x_guess + distance + 1,grid_w); x++)
                {
                    for (int y = Math.Max(y_guess - distance,0); y < Math.Min(y_guess + distance + 1,grid_h); y++)
                    {
                        if (data[x, y] == 'x')
                        {
                            temp_dist = Math.Sqrt((x_guess - x) * (x_guess - x) + (y_guess - y) * (y_guess - y));
                            if (temp_dist < min_dist)
                            {
                                min_dist = temp_dist;
                                position = new Point(x, y);
                            }
                        }
                    }
                
            }
            return position;
        }
        /// <summary>
        /// Finds the average angle of the significant vertical, and horizontal lines
        /// </summary>
        /// <param name="size">Represents the maximum radius in the accumulator array</param>
        /// <param name="accumulator">A 2D array which stores the number of pixels that fall on a particular line by theta and radius.</param>
        /// <param name="theta_avg_vert">A reference parameter that stores the average vertical angle of significant lines</param>
        /// <param name="theta_avg_hori">A reference parameter that stores the average horizontal angle for significant lines</param>
        private static void Find_Edges(int size, int[,] accumulator, ref int theta_avg_vert, ref int theta_avg_hori)
        {
            int count_hori = 0;
             int count_vert = 0;
            for (int i = 190; i >= 0 && (count_hori == 0 || count_vert == 0); i -= 20)
            {
                theta_avg_vert = 0;
                theta_avg_hori = 0;
                count_vert = 0;
                count_hori = 0;
                for (int x = 0; x < 180; x++)
                {
                    for (int y = 0; y < size * 2; y++)
                    {
                        if (accumulator[x, y] > i)
                        {
                            if (x < 45)
                            {
                                theta_avg_vert += x;
                                count_vert += 1;
                            }
                            else if (x > 135)
                            {
                                theta_avg_vert += x - 180;
                                count_vert += 1;
                            }
                            else
                            {
                                theta_avg_hori += x;
                                count_hori += 1;
                            }
                        }
                    }
                }
            }
            theta_avg_vert /= count_vert;
            theta_avg_hori /= count_hori;
        }
        /// <summary>
        /// Swaps two pointers (Mostly just to make the code a bit more readable)
        /// </summary>
        /// <param name="image_start">The first pointer to swap</param>
        /// <param name="swap_start">The second pointer to swap</param>
        private static void Swap(ref Byte* p1, ref Byte* p2)
        {
            p2 = (Byte*)((long)p2 + (long)p1);
            p1 = (Byte*)(p2 - p1);
            p2 = (Byte*)(p2 - p1);
        }
        /// <summary>
        /// Fills the accumulator with line data by applying a Hough transform.
        /// </summary>
        /// <param name="image_width">The width of the image being processed</param>
        /// <param name="image_height">The height of the image being processed</param>
        /// <param name="width">The width of the non-processable border around the outside of the image</param>
        /// <param name="image_start">A pointer to the beginning of the pixel data</param>
        /// <param name="image_stride">The width of each line of data. This accounts for padding on the edge of the pixel data</param>
        /// <param name="size">The maximum size of the radius of lines. Used to adjust the accumulator for negative lengths</param>
        /// <param name="accumulator">A reference parameter to the accumulator array. This will store the amount of pixels that fall on a line with a certain angle and radius</param>
        private static void Accumulate(int image_width, int image_height, int width, Byte* image_start, int image_stride, int size, int[,] accumulator)
        {
            
            System.Threading.Tasks.Parallel.For(width, image_width - width, delegate(int x)
            {
                
                System.Threading.Tasks.Parallel.For(width, image_height - width, delegate(int y)
                   {
                       if (*(image_start + y * image_stride + x * 4) == 255)
                       {
                           for (int theta = 0; theta < 180; theta += 1)
                           {
                               //Finds minimum distance from origin for lines in the form r = y*sin(theta)+x*cos(theta)
                               //Allows one to equate lines without dealing with any division by zero errors
                               accumulator[theta, size + (int)(y * Math.Sin((theta / 180.0) * Math.PI) + x * Math.Cos((theta / 180.0) * Math.PI))]++;
                           }
                       }
                   });
            });
        }
        /// <summary>
        /// Applies an adaptive threshold to an image.
        /// </summary>
        /// <param name="image_width">The width of the image</param>
        /// <param name="image_height">The height of the image</param>
        /// <param name="width">The width of the non-processable border around the outside of the image</param>
        /// <param name="image_start">A pointer to the start of the image data</param>
        /// <param name="image_stride">The size of a row of image data. Allows for padding at the ends</param>
        /// <param name="swap_start">A pointer to the begining of the output image data</param>
        /// <param name="swap_stride">The size of a row of image data in the output image</param>
        /// <param name="threshold">The threshold to apply using the adaptive threshold filter.</param>
        private static void Adaptive_Threshold(int image_width, int image_height, int width, Byte* image_start, int image_stride, Byte* swap_start, int swap_stride, int threshold)
        {
            int count;
            int total;
            Byte value;
            //Adaptive threshold just calculates the difference between a pixel's value, and the value of its neighbours
            //If it is above a certain threshold, it is determined to be a feature pixel, and set to white
            for (int x = width; x < image_width - width; x++)
            {
                for (int y = width; y < image_height - width; y++)
                {
                    total = 0;
                    count = 0;
                    for (int i = -width; i < width + 1; i++)
                    {
                        for (int t = -width; t < width + 1; t++)
                        {
                            total += *(image_start + (y + t) * image_stride + (x + i) * 4);
                            count++;
                        }
                    }
                    value = 0;

                    if ((total / count) - *(image_start + y * image_stride + x * 4) > threshold)
                    {
                        value = 255;
                        for (int i = -1; i < 2; i++)
                        {
                            for (int t = -1; t < 2; t++)
                            {
                                *(swap_start + (y + t) * swap_stride + (x + i) * 4) = 255;
                            }
                        }
                    }
                    *(swap_start + y * swap_stride + x * 4) = value;
                   
                }
            }
        }
       /// <summary>
       /// Used to find the median in a histogram of data
       /// </summary>
       /// <param name="histogram">An integer array storing the histogram data</param>
       /// <param name="size">The total of all columns in the histogram</param>
       /// <returns>The median of the histogram</returns>
        public static int histo_find(int[] histogram, int size)
        {
            size = size/2 + 1;  
            
            int c = 0;
            while (size > 0)
            {                
                size -= histogram[c++];
            }
            return c-1;
        }
        /// <summary>
        /// Applies a median filter to an image. The median filter will remove noise while maintaining edges in the image
        /// </summary>
        /// <param name="image_width">The width of the image being processed</param>
        /// <param name="image_height">The height of the image being processed</param>
        /// <param name="width">The width of the median filter to apply (width of 1 means 3x3 square, width  of 2 means 5x5 square, ...)</param>
        /// <param name="image_start">A pointer to the start of the input image data</param>
        /// <param name="image_stride">The size of a row of data in the input image</param>
        /// <param name="swap_start">A pointer to the start of the output image data</param>
        /// <param name="swap_stride">The size of a row of data in the output image</param>
        private static void Median_Filter(int image_width, int image_height, int width, Byte* image_start, int image_stride, Byte* swap_start, int swap_stride)
        {
            int count;            
            int[] neighbours = new int[(width * 2 + 1) * (width * 2 + 1)];
            count = (width * 2 + 1) * (width * 2 + 1);
            int[] histogram = new int[256];
            int x;
            //The median filter will substitute the value of each pixel with the median of its neighbours.
            //This is a little slower than a mean filter due to the median calculation, but will preserve edges
            for (int y = width; y < image_height - width; y++)
            {                
                for (int i = -width; i < width + 1; i++)
                {
                    for (int t = -width; t < width + 1; t++)
                    {
                        
                        histogram[(int)*(image_start + (y + t) * image_stride + (width + i) * 4)] += 1;
                    }
                }
                *(swap_start + y * swap_stride + width * 4)= (Byte)histo_find(histogram, count);                
                
                for (x = width+1; x < image_width - width; x++)
                {
                    for (int t = -width; t < width + 1; t++)
                    {
                        histogram[(int)*(image_start + (y + t) * image_stride + (x - width-1) * 4)] -= 1;
                    }
                    for (int t = -width; t < width + 1; t++)
                    {
                        histogram[(int)*(image_start + (y + t) * image_stride + (x + width) * 4)] += 1;
                    }
                    *(swap_start + y * swap_stride + x * 4)= (Byte)histo_find(histogram,count);
                }
                for (int i = -width; i < width + 1; i++)
                {
                    for (int t = -width; t < width + 1; t++)
                    {                        
                        histogram[(int)*(image_start + (y + t) * image_stride + (x + i-1) * 4)] = 0;
                    }
                }
                x = 0;
            }
        }
    }
}
