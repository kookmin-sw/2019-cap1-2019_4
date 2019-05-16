/*
 * Copyright (c) 2017, NVIDIA CORPORATION. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

// Kookmin University
// School of Computer Science
// Capstone #4 Flex Ads
// 20132651 Lee Sungjae

// Image 에 대한 Load, Save 와 관련된 함수가 저장된 loadImage.h 코드이다.
// 해당 코드에 이미지를 Crop 하여 저장하는 함수를 추가적으로 구현하였다.
// 해당 함수의 이름은 saveCropImageRGBA 이며, 추가적인 Parameter 를 입력받게 된다.

#ifndef __IMAGE_LOADER_H_
#define __IMAGE_LOADER_H_


#include "cudaUtility.h"


/**
 * Load a color image from disk into CUDA memory with alpha.
 * This function loads the image into shared CPU/GPU memory, using the functions from cudaMappedMemory.h
 *
 * @param filename Path to the image file on disk.
 * @param cpu Pointer to CPU buffer allocated containing the image.
 * @param gpu Pointer to CUDA device buffer residing on GPU containing image.
 * @param width Variable containing width in pixels of the image.
 * @param height Variable containing height in pixels of the image.
 *
 * @ingroup util
 */

bool loadImageRGBA( const char* filename, float4** cpu, float4** gpu, int* width, int* height );


/**
 * Save an image to disk
 * @ingroup util
 */
bool saveImageRGBA( const char* filename, float4* cpu, int y_min, int y_max, int x_min, int x_max, int width, int height, float max_pixel=255.0f );

/**
 * Save Cropped image to disk
 */
// saveImageRGBA 를 참고하여 새롭게 제작한 saveCropImageRGBA 함수이다.
// 추가적으로 bounding box 의 왼쪽 위 좌표와 오른쪽 아래 좌표를 입력받게 된다.
bool saveCropImageRGBA( const char* filename, float4* cpu, int y_min, int y_max, int x_min, int x_max, int width, int height, float max_pixel=255.0f );


/**
 * Load a color image from disk into CUDA memory.
 * This function loads the image into shared CPU/GPU memory, using the functions from cudaMappedMemory.h
 *
 * @param filename Path to the image file on disk.
 * @param cpu Pointer to CPU buffer allocated containing the image.
 * @param gpu Pointer to CUDA device buffer residing on GPU containing image.
 * @param width Variable containing width in pixels of the image.
 * @param height Variable containing height in pixels of the image.
 *
 * @ingroup util
 */
bool loadImageRGB( const char* filename, float3** cpu, float3** gpu, int* width, int* height, const float3& mean=make_float3(0,0,0) );


/**
 * Load a color image from disk into CUDA memory.
 * This function loads the image into shared CPU/GPU memory, using the functions from cudaMappedMemory.h
 *
 * @param filename Path to the image file on disk.
 * @param cpu Pointer to CPU buffer allocated containing the image.
 * @param gpu Pointer to CUDA device buffer residing on GPU containing image.
 * @param width Variable containing width in pixels of the image.
 * @param height Variable containing height in pixels of the image.
 *
 * @ingroup util
 */
bool loadImageBGR( const char* filename, float3** cpu, float3** gpu, int* width, int* height, const float3& mean=make_float3(0,0,0) );



#endif
