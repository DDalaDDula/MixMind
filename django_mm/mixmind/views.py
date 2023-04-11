# from django.db.models import F
# from django.db.models.functions import (
#     Power, 
#     Sqrt, 
#     Cast, 
#     Sum, 
#     Abs, 
#     Coalesce
# )
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import MusicRecommendSerializer
from .models import UserEmotion, MusicInfo, MusicEmotion
import numpy as np


class MusicRecommendViewSet(viewsets.ViewSet):
    def create(self, request):
        print(1)
        serializer = MusicRecommendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        emotion_values = request.data.get('emotionValues', [])
        user_emotion = UserEmotion.objects.create(
            love=emotion_values[0],
            joy=emotion_values[1],
            passion=emotion_values[2],
            happiness=emotion_values[3],
            sadness=emotion_values[4],
            anger=emotion_values[5],
            loneliness=emotion_values[6],
            longing=emotion_values[7],
            fear=emotion_values[8],
            surprise=emotion_values[9]
        )

        music_emotions = MusicEmotion.objects.all()

        music_emotions_similarity = []
        user_emotion_values = np.array([
            user_emotion.love,
            user_emotion.joy,
            user_emotion.passion,
            user_emotion.happiness,
            user_emotion.sadness,
            user_emotion.anger,
            user_emotion.loneliness,
            user_emotion.longing,
            user_emotion.fear,
            user_emotion.surprise
        ])
        for music_emotion in music_emotions:
            music_emotion_values = np.array([
                music_emotion.love,
                music_emotion.joy,
                music_emotion.passion,
                music_emotion.happiness,
                music_emotion.sadness,
                music_emotion.anger,
                music_emotion.loneliness,
                music_emotion.longing,
                music_emotion.fear,
                music_emotion.surprise
            ])
            cosine_similarity = np.dot(user_emotion_values, music_emotion_values) / (
                    np.linalg.norm(user_emotion_values) * np.linalg.norm(music_emotion_values))
            music_emotions_similarity.append((music_emotion, cosine_similarity))

        music_emotions_similarity.sort(key=lambda x: x[1], reverse=True)
        music_info_list = []
        for i in range(min(len(music_emotions_similarity), 10)):
            music_emotion = music_emotions_similarity[i][0]
            music_info = MusicInfo.objects.filter(id=music_emotion.musicId_id).first()
            if music_info:
                music_info_list.append(music_info)

        serializer = MusicRecommendSerializer(music_info_list, many=True)
        return Response(serializer.data)
