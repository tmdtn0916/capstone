from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import StoryRequest
from .serializers import StoryRequestSerializer
from openai import OpenAI
import openai

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
        
        