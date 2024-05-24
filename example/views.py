from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import mixins
from .models import Book
from .serializers import BookSerializer

# 함수형 뷰 FBV
@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")

@api_view(['GET', 'POST'])  #GET/POST 요청을 처리하게 만들어주는 데코레이터
def booksAPI(request):      # /book/
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True) #시리얼라이저에 전체 데이터를 한번에 집어넣기(직렬화, many=True)
        # many=True : 여러개를 입력했을 때 처리하도록 하는 옵션
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data) #POST 요청으로 들어온 데이터를 시리얼라이저에 집어넣기
        if serializer.is_valid(): #유효한 데이터라면,
            serializer.save()   # 시리얼라이저의 역직렬화를 통해 save(), 모델시리얼라이저의 기본 create() 함수가 동작
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 201메시지를 보내며 성공!
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400 잘못된 요청.

@api_view(['GET'])
def bookAPI(request, bid): # /book/bid/
    book = get_object_or_404(Book, bid=bid) # bid=bid 인 데이터를 Book 에서 가져오고, 없으면 404 에러
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

#클래스형 뷰 CBV
class BooksAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookAPI(APIView):
    def get(self, request, bid):
        book = get_object_or_404(Book, bid=bid)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

#클래스형 뷰 CBV -> mixins 사용
class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):    # GET 메소드 처리 함수(전체 목록)
        return self.list(request, *args, **kwargs) # mixins.ListModelMixin과 연결
    def post(self, request, *args, **kwargs):   # POST 메소드 처리 함수(1권 등록)
        return self.create(request, *args, **kwargs) # mixins.CreateModelMixin과 연결

class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid' # "bid"를 primary key(pk) 로 설정

    def get(self, request, *args, **kwargs):    # GET method 처리 함수(1권)
        return self.retrieve(request, *args, **kwargs) # mixins.RetrieveModelMixin 과 연결
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#클래스형 뷰 CBV -> mixins 사용한 것 보다도 generics를 사용할 경우 더 간단하게 코드를 작성할 수 있다.
class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'