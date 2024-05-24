# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .serializers import RecommendationSerializer
# import json
# import pickle
# import pandas as pd
# import numpy as np

# # Load the pickled files
# with open('models/train_df.pkl', 'rb') as f:
#     train_df = pickle.load(f)
# with open('models/cosine_sim.pkl', 'rb') as g:
#     cosine_sim = pickle.load(g)

# def recommend_wedding_planners_logic(City, CategoryName, cosine_sim=cosine_sim):
#     indices = train_df.index[(train_df['City'] == City) & (train_df['CategoryName'] == CategoryName)]
#     sim_scores = list(enumerate(cosine_sim[indices[0]]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:]  # similar wedding planners
#     wedding_indices = [i[0] for i in sim_scores]
#     top_planners = train_df.iloc[wedding_indices][['Name', 'Location', 'City', 'CategoryName', 'Image', 'Phone', 'avg_ratings']]
#     filtered_planners = top_planners[(top_planners['City'] == City) & (top_planners['CategoryName'] == CategoryName)]
#     filtered_planners = filtered_planners.sort_values(by='avg_ratings', ascending=False)  # Sort by rating
#     final_recommended = filtered_planners[['Name', 'Location', 'City', 'CategoryName', 'Image', 'Phone', 'avg_ratings']].to_dict(orient='records')
#     return final_recommended

# @api_view(['POST'])
# def recommend_wedding_planners(request):
#     try:
#         data = request.data
#         city = data.get('city')
#         category_name = data.get('category_name')
#         if not city or not category_name:
#             return Response({'error': 'City and CategoryName are required parameters'}, status=400)
#         recommendations = recommend_wedding_planners_logic(city, category_name)
#         serializer = RecommendationSerializer(recommendations, many=True)
#         return Response({'recommendations': serializer.data}, status=200)
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import RecommendationRequestSerializer, RecommendationSerializer
import pickle
import pandas as pd
import numpy as np

# Load the pickled files
with open('models/train_df.pkl', 'rb') as f:
    train_df = pickle.load(f)
with open('models/cosine_sim.pkl', 'rb') as g:
    cosine_sim = pickle.load(g)

def recommend_wedding_planners_logic(City, CategoryName, cosine_sim=cosine_sim):
    indices = train_df.index[(train_df['City'] == City) & (train_df['CategoryName'] == CategoryName)]
    sim_scores = list(enumerate(cosine_sim[indices[0]]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]  # similar wedding planners
    wedding_indices = [i[0] for i in sim_scores]
    top_planners = train_df.iloc[wedding_indices][['Name', 'Location', 'City', 'CategoryName', 'Image', 'Phone', 'avg_ratings']]
    filtered_planners = top_planners[(top_planners['City'] == City) & (top_planners['CategoryName'] == CategoryName)]
    filtered_planners = filtered_planners.sort_values(by='avg_ratings', ascending=False)  # Sort by rating
    final_recommended = filtered_planners[['Name', 'Location', 'City', 'CategoryName', 'Image', 'Phone', 'avg_ratings']].to_dict(orient='records')
    return final_recommended

@swagger_auto_schema(
    method='post',
    request_body=RecommendationRequestSerializer,
    responses={200: RecommendationSerializer(many=True)},
    operation_description="Provide city and category_name to get recommendations. City should be the one user entered during signup,and make sure that user have only option of city name that are mentioned on dataset while signup, and category_name should match the category_template and category_name on dataset you provided to me. Note: Each and every spelling should be correct if not then it will show error "
)
@api_view(['POST'])
def recommend_wedding_planners(request):
    try:
        serializer = RecommendationRequestSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            category_name = serializer.validated_data['category_name']
            recommendations = recommend_wedding_planners_logic(city, category_name)
            response_serializer = RecommendationSerializer(recommendations, many=True)
            return Response({'recommendations': response_serializer.data}, status=200)
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
