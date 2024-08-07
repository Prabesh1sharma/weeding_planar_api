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
    # Check if the city and category name exist in the dataset
    if City not in train_df['City'].values or CategoryName not in train_df['CategoryName'].values:
        return None

    indices = train_df.index[(train_df['City'] == City) & (train_df['CategoryName'] == CategoryName)]
    
    # If no matching index found, return None
    if len(indices) == 0:
        return None

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
    operation_description="Provide city and category_name to get recommendations. City should be the one user entered during signup, and make sure that user has only the option of city names that are mentioned in the dataset while signup, and category_name should match the category_template and category_name in the dataset you provided to me. Note: Each and every spelling should be correct if not then it will show error."
)
@api_view(['POST'])
def recommend_wedding_planners(request):
    try:
        serializer = RecommendationRequestSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            category_name = serializer.validated_data['category_name']
            # recommendations = recommend_wedding_planners_logic(city, category_name)
            recommendations = "hello guys whats up"
            
            if recommendations is None:
                return Response({'error': "No data found, city name or category_name doesn't match with database"}, status=404)

            response_serializer = RecommendationSerializer(recommendations, many=True)
            return Response({'recommendations': response_serializer.data}, status=200)
        
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
