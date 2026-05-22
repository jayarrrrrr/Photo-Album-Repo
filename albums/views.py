from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm


class IsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = getattr(self, 'object', None)
        user = self.request.user
        if user.is_superuser:
            return True
        # If object has owner attribute
        if obj is None:
            # for CreateView allow authenticated
            return user.is_authenticated
        owner = getattr(obj, 'owner', None)
        if owner and owner == user:
            return True
        # check group membership
        return user.groups.filter(name='AlbumAdmin').exists()


class AlbumListView(ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.object.pk})


class AlbumUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.object.pk})


class AlbumDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('albums:list')


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_pk'] = self.kwargs['album_pk']
        return context

    def form_valid(self, form):
        album = Album.objects.get(pk=self.kwargs['album_pk'])
        form.instance.album = album
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.kwargs['album_pk']})


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.album.owner == user or user.groups.filter(name='AlbumAdmin').exists() or user.is_superuser

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.object.album.pk})
