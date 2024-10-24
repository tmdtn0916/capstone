from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import StoryRequest
from .serializers import StoryRequestSerializer, UserSerializer
from openai import OpenAI
import openai, logging
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import urllib.request

logger = logging.getLogger(__name__)

class StoryRequestViewSet(viewsets.ModelViewSet):
    queryset = StoryRequest.objects.all()
    serializer_class = StoryRequestSerializer

    @action(detail=False, methods=['post'])
    def generate_story(self, request):
        keywords = request.data.get('keywords')
        client = OpenAI(
        api_key=openai.api_key,
        )

        # few-shot 프롬프트 엔지니어링 적용
        example_stories = [
            {
                "keywords": "고양이, 모험, 우정",
                "story": "옛날 옛적에, 모험을 좋아하는 고양이 한 마리가 있었습니다. \n그 고양이는 친구들과 함께 숲을 탐험하며 많은 모험을 했습니다. \n그들은 서로 도우며 우정을 쌓아갔습니다."
            },
            {
                "keywords": "토끼, 마법, 용기",
                "story": "한 작은 마을에 용감한 토끼가 살고 있었습니다.\n 어느 날, 마을에 마법의 문제가 생겼습니다. \n토끼는 용기를 내어 마법을 풀기 위해 모험을 떠났고, 결국 마을을 구했습니다."
            }
        ]

        # 프롬프트 생성
        example_prompts = "\n".join(
            f"Keywords: {example['keywords']}\nStory: {example['story']}\n"
            for example in example_stories
        )
        
        # 사용자 입력 키워드 추가
        prompt = f"""You are the best children's book writer.
                    Create a children's story in Korean with these keywords: {keywords}
                    {example_prompts}
                    Keywords: {keywords}
                    Story: """



        try:
            response =client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are the best children's book writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            # choice = response['choices'][0]
            # story = choice['message']['content']
            story = response.choices[0].message.content
            print("story: \n"+story)
            return Response({"story": story})
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=500)
        


@api_view(['POST'])
def user_signup(request):
    logger.debug("Received data: %s", request.data)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        logger.debug("Errors: %s", serializer.errors)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    logger.debug("Received data: %s", request.data)

    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password = password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token' : token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error' : 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def plot_view(request):
    if request.method == 'POST':

        keywords = request.data.get('storyIdea')
        client = OpenAI(
        api_key=openai.api_key,
        )

        # few-shot 프롬프트 엔지니어링 적용
        example_stories = [
            {
                "keywords": "고양이, 모험, 우정",
                "story": "옛날 옛적에, 모험을 좋아하는 고양이 한 마리가 있었습니다. \n그 고양이는 친구들과 함께 숲을 탐험하며 많은 모험을 했습니다. \n그들은 서로 도우며 우정을 쌓아갔습니다."
            },
            {
                "keywords": "토끼, 마법, 용기",
                "story": "한 작은 마을에 용감한 토끼가 살고 있었습니다.\n 어느 날, 마을에 마법의 문제가 생겼습니다. \n토끼는 용기를 내어 마법을 풀기 위해 모험을 떠났고, 결국 마을을 구했습니다."
            }
        ]

        # 프롬프트 생성
        example_prompts = "\n".join(
            f"Keywords: {example['keywords']}\nStory: {example['story']}\n"
            for example in example_stories
        )
        
        # 사용자 입력 키워드 추가
        prompt = f"""You are the best children's book writer.
            Create a children's story in Korean with these keywords: {keywords}.
            The story should be concise and no longer than 100 characters.
            {example_prompts}
            Keywords: {keywords}
            Story: """

        try:
            response =client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are the best children's book writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            # choice = response['choices'][0]
            # story = choice['message']['content']
            story = response.choices[0].message.content
            print("story: \n"+story)            

            response2 = client.images.generate(
                model="dall-e-3",
                prompt=story,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response2.data[0].url
            img_dest = "./images/"
            urllib.request.urlretrieve(image_url, img_dest+"result.jpg")
            
            print("---------------------- return --------------------")
            return Response({"story": story}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=500)

        # return Response({"message": "Story created successfully"}, status=status.HTTP_201_CREATED)