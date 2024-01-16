# recommendations/recommendations.py
from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
        BookRecommendation(id=4, title="Автостопом по Галактике"),
        BookRecommendation(id=5, title="Виноватые звёзды"),
        BookRecommendation(id=6, title="Гадкие лебеди"),
        BookRecommendation(id=7, title="Границы бесконечности"),
        BookRecommendation(id=8, title="Гроза в Безначалье"),
        BookRecommendation(id=9, title="Гроздья гнева"),
        BookRecommendation(id=10, title="Дайте им умереть"),

    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(
            id=1, title="The Hitchhiker's Guide to the Galaxy"
        ),
        BookRecommendation(id=2, title="Ender's Game"),
        BookRecommendation(id=3, title="The Dune Chronicles"),
        BookRecommendation(id=4, title="Дети полуночи"),
        BookRecommendation(id=5, title="Зов предков"),
        BookRecommendation(id=6, title="Иное небо"),
        BookRecommendation(id=7, title="Колыбель для кошки"),
        BookRecommendation(id=8, title="Королева Ойкумены"),
        BookRecommendation(id=9, title="Кровавый меридиан"),
        BookRecommendation(id=10, title="Механизм пространства"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(
            id=7, title="The 7 Habits of Highly Effective People"
        ),
        BookRecommendation(
            id=8, title="How to Win Friends and Influence People"
        ),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
        BookRecommendation(id=7, title="На Западном фронте без перемен"),
        BookRecommendation(id=7, title="Над пропастью во ржи"),
        BookRecommendation(id=7, title="Обитаемый остров"),
        BookRecommendation(id=7, title="Опоздавшие к лету"),
        BookRecommendation(id=7, title="Осколки чести"),
        BookRecommendation(id=7, title="Пасынки Вселенной"),
        BookRecommendation(id=7, title="Пикник на обочине"),
    ],
}

class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        print(len(books_for_category))
        print(request.max_results)
        print(num_results)
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()