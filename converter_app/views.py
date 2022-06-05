from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Movies, Image_Compress, Task
from .forms import TaskForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def movie_mining(request):
    page = requests.get("https://mlwbd.top/")
    soup = BeautifulSoup(page.content, "html.parser")
    # all five rows
    all_movies = soup.find(id="dtw_content-6")
    # title, links and images of those latest movies
    titles = [name.find('h3').get_text() for name in all_movies.find_all(class_="w_item_b")]
    links = [link['href'] for link in all_movies.find_all('a', href=True) if link.text]
    thumbnails = [image['src'] for image in all_movies.find_all('img', src=True)]
    images = [thumbnails[i] for i in range(len(thumbnails)) if i % 2 != 0]
    #all movies data in list and dictonary format
    movies = [{'name': titles[i], 'link': links[i], 'image': images[i]} for i in range(len(titles))]   
    
    # for i in range(len(titles)):
    #     movie_obj = Movies(title=titles[i], link=links[i], image=images[i])
    #     movie_obj.save()
    movie_obj = Movies.objects.all()
    print(movie_obj[4].title)
    new_status = ""
    
    for movie in movie_obj:
        for i in range(len(titles)):
            if movie.link not in links:
                new_status = "New"
                for moviee in movie_obj:
                    for i in range(len(movie_obj)):
                        movie_obj[i].title = titles[i]
                        movie_obj[i].link = links[i]
                        movie_obj[i].image = images[i]
                        movie_obj[i].save()
            
    
    context={'movies': Movies.objects.all(), 'is_new': new_status}
    return render(request, 'movie_mining.html', context)

# image compressor start here
def image_compressor(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        try:
            image_obj = Image_Compress(image=image)
            image_obj.save()
            IMG = Image_Compress.objects.get(id=image_obj.id)
            return render(request, 'img_compress.html', {'image_obj': IMG})
        except:
            print('Please, Enter valid image')
    
    if request.method == 'GET':
        image_link = request.GET.get('view_link')
        return render(request, 'img_compress.html', {'view_image': image_link})
    return render(request, 'img_compress.html')

def to_do(request):
    tasks = Task.objects.all()
    task_form = TaskForm()
    
    context = {'tasks': tasks, 'task_form': task_form}
    return render(request, 'to-do.html', context)