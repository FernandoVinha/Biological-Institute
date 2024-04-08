import cv2
import numpy as np
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Photo
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user

            # Ler a imagem para processamento OpenCV
            uploaded_image = cv2.imdecode(np.fromstring(request.FILES['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)

            # Converte para escala de cinza e aplica threshold
            cinza = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY_INV)

            # Encontra contornos na imagem
            contornos, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Calcula a área média dos contornos encontrados
            areas = [cv2.contourArea(c) for c in contornos]
            area_media = np.mean(areas)

            # Define o limiar para o tamanho do ponto
            limiar_tamanho = area_media * 1.6

            # Inicializa o contador
            contador_total = 0

            for contorno in contornos:
                area_contorno = cv2.contourArea(contorno)
                (x, y), raio = cv2.minEnclosingCircle(contorno)
                centro = (int(x), int(y))
                raio = int(raio)

                if area_contorno > limiar_tamanho:
                    contador_total += 2
                else:
                    contador_total += 1

                # Desenha um círculo vermelho em volta do ponto
                cv2.circle(uploaded_image, centro, raio, (0, 0, 255), 2)

            # Adiciona a contagem total na imagem
            posicao_texto = (10, uploaded_image.shape[0] - 10)
            cv2.putText(uploaded_image, f"Total: {contador_total}", posicao_texto, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Salva a imagem processada em um objeto ContentFile
            _, buffer = cv2.imencode('.jpeg', uploaded_image)
            processed_image_file = ContentFile(buffer.tobytes(), 'processed_image.jpeg')

            photo.count_field = contador_total
            photo.processed_image = processed_image_file
            photo.save()

            # Redirecionar para uma página de sucesso ou de detalhes
            return redirect('photo_list')  # Substitua 'pagina_de_sucesso' pela sua URL desejada

    else:
        form = PhotoForm()
    return render(request, 'upload_photo.html', {'form': form})


@login_required  # Garante que apenas usuários logados possam acessar essa view
def photo_list(request):
    # Filtra as fotos para mostrar apenas as do usuário logado
    photos_list = Photo.objects.filter(uploaded_by=request.user).order_by('upload_date')  
    paginator = Paginator(photos_list, 10)  # Mostra 10 fotos por página

    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)

    return render(request, 'photo_list.html', {'photos': photos})


@require_POST
@login_required
def update_count(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, uploaded_by=request.user)
    form = ManualCountForm(request.POST, instance=photo)
    if form.is_valid():
        form.save()
        return redirect('photo_list')
    else:
        return redirect('photo_list')  # Ou alguma outra forma de lidar com o form inválido

@require_POST
@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if photo.uploaded_by != request.user:
        return HttpResponseForbidden()  # Retorna um erro 403
    photo.delete()
    return redirect('photo_list')