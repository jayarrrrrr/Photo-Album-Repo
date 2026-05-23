from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404
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


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully. You can now log in.')
        return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.album.owner == user or user.groups.filter(name='AlbumAdmin').exists() or user.is_superuser or user.is_superuser

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.object.album.pk})


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            messages.warning(request, "Photo not found. It may have been deleted already.")
            return redirect('albums:list')

    def get_object(self, queryset=None):
        # Prefer an already-loaded object (set in test_func) to avoid additional DB hits
        obj = getattr(self, 'object', None)
        if obj is not None:
            return obj
        # Safely fetch the photo without raising Http404 here
        pk = self.kwargs.get('pk')
        return Photo.objects.filter(pk=pk).select_related('album__owner').first()

    def test_func(self):
        # Avoid calling get_object() which may raise Http404; fetch safely instead
        pk = self.kwargs.get('pk')
        obj = Photo.objects.filter(pk=pk).select_related('album__owner').first()
        if not obj:
            # Let handle_no_permission handle the user-visible response
            return False
        # cache the object for later use by get_object/delete
        self.object = obj
        user = self.request.user
        return obj.album.owner == user or user.groups.filter(name='AlbumAdmin').exists() or user.is_superuser

    def handle_no_permission(self):
        # Called when test_func returns False — redirect with a helpful message
        messages.warning(self.request, "Photo not found or you don't have permission to delete it.")
        return redirect('albums:list')

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.object.album.pk})
