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

// 기존 코드에는 포함되지 않은 loadImage.h 모듈을 추가적으로 가져온다.
// 해당 모듈의 saveImageRGBA 함수를 이용하여 이미지를 Local 에 저장하기 위함이다.
#include "gstCamera.h"
#include "loadImage.h"

#include "glDisplay.h"
#include "glTexture.h"

#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#include "cudaMappedMemory.h"
#include "cudaNormalize.h"
#include "cudaFont.h"

#include "detectNet.h"

// Real-Time Detection 을 위한 기본 카메라 모듈은 Jetson 에 장착된 onboard camera 를 사용한다.
// -1 for onboard camera, or change to index of /dev/video V4L2 camera (>=0)
#define DEFAULT_CAMERA -1


bool signal_recieved = false;

// camera signal 이 정상적으로 작동하는지 체크하기 위한 함수이다.
void sig_handler(int signo)
{
	if( signo == SIGINT )
	{
		printf("received SIGINT\n");
		signal_recieved = true;
	}
}


int main( int argc, char** argv )
{
	// 인자로 deep learning model 이름을 받아와
	// 해당 model 을 기반으로 하는 코드를 실행한다.
	printf("detectnet-camera\n  args (%i):  ", argc);

	for( int i=0; i < argc; i++ )
		printf("%i [%s]  ", i, argv[i]);

	printf("\n\n");

	// camera 시그널을 체크하고, 만약 시그널이 정상적으로 잡히지 않았다면
	// 시그널이 잡히지 않는다는 메시지를 출력한다.
	if( signal(SIGINT, sig_handler) == SIG_ERR )
		printf("\ncan't catch SIGINT\n");

	// gstCamera 를 이용하여 camera device 객체를 생성한다.
	gstCamera* camera = gstCamera::Create(DEFAULT_CAMERA);

	// camera 객체가 정상적으로 생성되지 않았다면, camera initialize 에 실패하였다는 메시지를 출력한다.
	if( !camera )
	{
		printf("\ndetectnet-camera:  failed to initialize video device\n");
		return 0;
	}

	// 여기까지 문제 없이 실행되었다면, 성공적으로 camera init이 진행되었음을 출력한다.
	// 현재 camera 에서 입력받는 영상의 너비와 높이, Pixel Depth(color channel)를 출력한다.
	printf("\ndetectnet-camera:  successfully initialized video device\n");
	printf("    width:  %u\n", camera->GetWidth());
	printf("   height:  %u\n", camera->GetHeight());
	printf("    depth:  %u (bpp)\n\n", camera->GetPixelDepth());

	// Deep Learning 모델을 이용한 Detection 을 수행하는
	// detectNet 객체를 net 이름으로 생성한다.
	// 이 때, 프로그램 실행 시 입력받은 값으로 지정된 모델을 생성하게 된다.
	detectNet* net = detectNet::Create(argc, argv);

	// 만약 detectNet 객체가 생성되지 못했다면, 에러 메시지를 출력한다.
	if( !net )
	{
		printf("detectnet-camera:   failed to initialize imageNet\n");
		return 0;
	}

	// 최대 그려질 수 있는 Bounding Box 개수의 크기와
	// 현재 detect 하는 class 의 개수를 detectNet 객체로부터 받아온다.
	const uint32_t maxBoxes = net->GetMaxBoundingBoxes();
	const uint32_t classes  = net->GetNumClasses();

	// Bounding Box 데이터와 confidence 데이터가 저장될 공간을 메모리에 할당한다.
	float* bbCPU    = NULL;
	float* bbCUDA   = NULL;
	float* confCPU  = NULL;
	float* confCUDA = NULL;

	// 해당 공간을 할당하는 동시에, 실패할 경우 에러 메시지를 출력한다.
	if( !cudaAllocMapped((void**)&bbCPU, (void**)&bbCUDA, maxBoxes * sizeof(float4)) ||
	    !cudaAllocMapped((void**)&confCPU, (void**)&confCUDA, maxBoxes * classes * sizeof(float)) )
	{
		printf("detectnet-console:  failed to alloc output memory\n");
		return 0;
	}

	//openGL 을 이용하여 실시간으로 얼굴을 Detect 하고 Bounding Box 가 그려지는 영상을 출력한다.
	// openGL 의 Display 객체를 display 이름으로 생성한다.
	glDisplay* display = glDisplay::Create();
	glTexture* texture = NULL;

	// 정상적으로 생성되지 않았을 경우, 에러 메시지를 출력한다.
	// 정상적으로 생성되었을 경우, 입력 camera 크기에 맞추어 texture 를 생성한다.
	if( !display ) {
		printf("\ndetectnet-camera:  failed to create openGL display\n");
	}
	else
	{
		texture = glTexture::Create(camera->GetWidth(), camera->GetHeight(), GL_RGBA32F_ARB/*GL_RGBA8*/);
		if( !texture )
			printf("detectnet-camera:  failed to create openGL texture\n");
	}

	// cuda font 는 image 위에 text 나 image 를 추가적으로 rendering 하기 위한 것으로 보인다.
	// 하지만 본 코드에서는 font 가 추가적으로 사용되지 않았다.
	cudaFont* font = cudaFont::Create();

	// camera 를 Open 하여 streaming 을 시작하며, Open 되지 않을 경우 에러 메시지를 출력한다.
	if( !camera->Open() )
	{
		printf("\ndetectnet-camera:  failed to open camera for streaming\n");
		return 0;
	}

	printf("\ndetectnet-camera:  camera open for streaming\n");

	// conf 지정값이 있어 필요 없을 것으로 생각되는 코드이다.
	float confidence = 0.0f;

	// 10초 주기로 image 를 cropping 하여 저장하기 위한 코드이다.
	// bool 은 milli sec 을 무시하기 위한 것이다.
	bool time_flag = true;
	char zero = '0';
	char one = '1';

	// signal 이 입력되는 동안 계속해서 camera 로부터 streaming 을 입력받는다.
	while( !signal_recieved )
	{
		// imgCPU 와 imgCUDA 는 camera 로 입력받은 이미지가 저장되는 곳이다.
		// 일반적인 RGBA 이미지가 아닌, camera 에서 입력 받은 직후의 YUV 이미지 데이터이다.
		void* imgCPU  = NULL;
		void* imgCUDA = NULL;

		// get the latest frame
		// 한 프레임을 camera로부터 입력받아 생성한 이미지 객체에 저장한다.
		if( !camera->Capture(&imgCPU, &imgCUDA, 1000) )
			printf("\ndetectnet-camera:  failed to capture frame\n");

		// convert from YUV to RGBA
		// YUV 이미지를 RGBA 로 변환한다.
		// 이 때, imgRGBA 를 saveImageRGBA 함수를 이용하여 저장하기 위해서는
		// ConvertRGBA 함수의 3번째 인자를 true 로 추가적으로 작성해 주어야 한다.
		void* imgRGBA = NULL;

		if( !camera->ConvertRGBA(imgCUDA, &imgRGBA, true) )
			printf("detectnet-camera:  failed to convert from NV12 to RGBA\n");

		int numBoundingBoxes = maxBoxes;
        
		// filename with string object
		// 이미지 데이터를 저장하기 위해 저장될 이미지 파일명을 detect 된 시간으로 지정한다.
		// 먼저 curTime 을 이용하여 milli 초를 계산하여 milli 변수에 저장한다.
		timeval curTime;
		gettimeofday(&curTime, NULL);
		int milli = curTime.tv_usec / 1000;

		// 현재 시간을 local time 에 맞추어 now 변수에 저장한다.
		time_t t = time(0);
		struct tm* now = localtime(&t);

		// 밀리초를 제외한 파일명(년, 월, 일, 시, 분, 초)를 buffer 배열에 저장한다.
		// strftime 을 이용하여 now 로부터 시간을 가져와 buffer 에 저장한다.
		char buffer[80];
		strftime(buffer, 80, "%Y%m%d-%H%M%S", now);

		// 밀리초와 이미지 확장자를 추가하여 filename 배열에 저장한다.
		char filename[100];
		sprintf(filename, "%s%d.PNG", buffer, milli);

		// 앞에서 생성한 detectNet 객체인 net 을 이용하여 Capture 된 이미지 객체를 Detect 를 이용해 분석한다.
		// 이 때, bbCPU 에 물체가 detect 된 좌표를 순차적으로 저장한다.
		if( net->Detect((float*)imgRGBA, camera->GetWidth(), camera->GetHeight(), bbCPU, &numBoundingBoxes, confCPU))
		{
			// 몇 개의 물체가 detect 되었는지 출력한다.
			printf("%i bounding boxes detected\n", numBoundingBoxes);

			int lastClass = 0;
			int lastStart = 0;

			// 모든 bounding box 를 순회하며 그리기 위한 코드이다.
			for( int n=0; n < numBoundingBoxes; n++ )
			{

				const int nc = confCPU[n*2+1];
				float* bb = bbCPU + (n * 4);

				// 각각의 bounding box 가 어떤 클래스를 어느정도의 신뢰도로 detect 한 것인지 출력한다.
				printf("detected obj %i  class #%u (%s)  confidence=%f\n", n, nc, net->GetClassDesc(nc), confCPU[n*2]);

				// 각각의 bounding box 의 좌표와 너비, 높이를 출력한다.
				printf("bounding box %i  (%f, %f)  (%f, %f)  w=%f  h=%f\n", n, bb[0], bb[1], bb[2], bb[3], bb[2] - bb[0], bb[3] - bb[1]);

				// detect 된 bounding box 부분을 cropping 하여 local 에 filename 으로 저장하는 코드이다.
				// Cropping 된 이미지를 저장하기 위해 saveCropImageRGBA 함수를 새롭게 loadImage 에 작성하였다.
				// saveCropImageRGBA 는 saveImageRGBA 와 다르게 좌표를 추가적으로 입력받으며, 해당 위치를 기준으로 이미지를 Cropping 하여 저장한다.
				
				// 10초를 주기로 cropping 된 이미지를 저장하기 위하여,
				// filename 의 sec 부분을 추출해 내어 0의 자리이면 저장하는 방법을 사용한다.
				// 현재 방법으로는 특정 시점에만 이미지가 저장되기 때문에, 더 정교한 방법의 고안이 필요하다.
				char now_sec = filename[14];
				if(now_sec == zero && time_flag == true)
				{
					saveCropImageRGBA(filename, (float4*)imgRGBA, bb[1], bb[3], bb[0], bb[2], camera->GetWidth(), camera->GetHeight(), 255.0f);
					time_flag = false;
				}
				if(now_sec == one && time_flag == false)
				{
					time_flag = true;
				}

				// detectNet 의 DrawBoxes 를 이용하여 인식된 Bounding Box 를 이미지에 표시하여 imgRGBA 에 저장한다.
				if( nc != lastClass || n == (numBoundingBoxes - 1) )
				{
					if( !net->DrawBoxes((float*)imgRGBA, (float*)imgRGBA, camera->GetWidth(), camera->GetHeight(),
						                        bbCUDA + (lastStart * 4), (n - lastStart) + 1, lastClass) )
						printf("detectnet-console:  failed to draw boxes\n");

					lastClass = nc;
					lastStart = n;

					CUDA(cudaDeviceSynchronize());
				}
			}

			// display 가 NULL 이 아니면, 현재 어떤 Frame 속도로 Rendering 되는지 Title 에 표시한다.
			if( display != NULL )
			{
				char str[256];
				sprintf(str, "TensorRT %i.%i.%i | %s | %04.1f FPS", NV_TENSORRT_MAJOR, NV_TENSORRT_MINOR, NV_TENSORRT_PATCH, precisionTypeToStr(net->GetPrecision()), display->GetFPS());
				display->SetTitle(str);
			}
		}


		// update display
		// display 가 NULL 이 아니면, display 를 rendering 한다.
		if( display != NULL )
		{
			display->UserEvents();
			display->BeginRender();

			if( texture != NULL )
			{
				// rescale image pixel intensities for display
				// display 에 출력하기 위해 RGBA 이미지를 rescale 하는 과정이다.
				CUDA(cudaNormalizeRGBA((float4*)imgRGBA, make_float2(0.0f, 255.0f),
								   (float4*)imgRGBA, make_float2(0.0f, 1.0f),
		 						   camera->GetWidth(), camera->GetHeight()));

				// map from CUDA to openGL using GL interop
				void* tex_map = texture->MapCUDA();

				if( tex_map != NULL )
				{
					cudaMemcpy(tex_map, imgRGBA, texture->GetSize(), cudaMemcpyDeviceToDevice);
					texture->Unmap();
				}

				// draw the texture
				// 처리가 완료된 texture 를 최종적으로 Render 한다.
				texture->Render(100,100);
			}

			display->EndRender();
		}
	}

	printf("\ndetectnet-camera:  un-initializing video device\n");



	// signal 이 종료되고 camera, display 가 NULL 이 아니면 해당 객체를 delete 한다.
	if( camera != NULL )
	{
		delete camera;
		camera = NULL;
	}

	if( display != NULL )
	{
		delete display;
		display = NULL;
	}

	// 프로그램 종료 메시지를 출력한다.
	printf("detectnet-camera:  video device has been un-initialized.\n");
	printf("detectnet-camera:  this concludes the test of the video device.\n");
	return 0;
}
