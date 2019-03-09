// AWS SDK for C++ Test
// List My Buckets
// Commented by Sungjae Lee

// AWS 와 연결하기 위한 헤더 파일을 불러온다.
#include <aws/core/Aws.h>
#include <aws/s3/S3Client.h>
#include <aws/s3/model/Bucket.h>

int main(int argc, char const *argv[]) {

    // AWS SDK 는 Init 과 Shutdown 과정이 필요하다
    // 이 때, 어떤 Option 으로 초기화할지 정하기 위해서 Option 정보를 가져온다.
    // option 은 세부적으로 logging level 이나 memory manage 를 설정 가능하다.
    Aws::SDKOptions options;
    Aws::InitAPI(options);

    {
        // S3 서버와 통신하기 위한 S3Client 객체를 생성한다.
        // 해당 객체의 ListBuckets 함수를 이용하여 Bucket 목록을 가져온다.
        Aws::S3::S3Client s3_client;
        auto outcome = s3_client.ListBuckets();

        // Bucket 의 이름을 출력하기 위해, 다수의 Bucket 정보를 Vector 자료구조에 저장한다.
        // 저장된 정보는 for 문에 의해 순회되며, 이름만 가져와 출력하게 된다.
        std::cout << "Buckets" << '\n';
        Aws::Vector<Aws::S3::Model::Bucket> b_list = outcome.GetResult().GetBuckets();
        for(auto const &bucket : b_list){
            std::cout << bucket.GetName() << '\n';
        }
        // 작성된 코드는 outcome 변수가 정상적으로 Bucket 정보를 가져왔을 때만 작동하며
        // 문제가 발생하지 않도록 IsSuccess 함수를 이용해 예외처리를 해줄 필요가 있다.
        // 해당 코드는 aws_sdk_for_cpp example 코드를 참고하여 작성되었다.
    }
    AWS::ShutdownAPI(options);
    return 0;
}
