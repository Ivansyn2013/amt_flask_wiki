// Файл: static/js/_video_player.js
"use strict";

class VideoPlayerManager {
    constructor(playerId = 'main-player') {
        this.playerId = playerId;
        this.player = null;
        this.currentVideo = null;
        this.isMinimized = false;
        this.isPlaylistVisible = true;
        this.domElements = {};
        this.hasInitialized = false;
        this.hasLoadedFirstVideo = false;
        this.videoElement = null;
        this.isHidden = false
        this.init();
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('toggle-player') &&
                !this.isHidden &&
                this.hasInitialized) {
                this.expand();
            }
            else {
                this.show()
            }

        });
    }

    init() {
        this.cacheDomElements();
        this.initPlyr();
        this.bindEvents();
        // this.loadFirstVideo();
        this.hasInitialized = true;
        console.log("Plyer initialising")
    }

    cacheDomElements() {
        this.domElements = {
            container: document.getElementById('video-player-container'),
            header: document.querySelector('.video-player-header'),
            togglePlayerBtn: document.querySelector('.toggle-player'),
            togglePlaylistBtn: document.querySelector('.toggle-playlist'),
            closePlayerBtn: document.querySelector('.close-player'),
            nowPlayingTitle: document.getElementById('now-playing-title'),
            playlistItems: document.querySelectorAll('.playlist-item'),
            videoElement: document.getElementById(this.playerId)
        };
    }

    initPlyr() {
        // const videoElement = this.domElements.videoElement;
        const videoElement = document.getElementById('main-video-player');

        if (!videoElement) {
            console.error('Video element not found!');
            console.error('❌ Video element not found!');
            console.log('Available video elements:');
            allVideos.forEach(video => {
                console.log('-', video.id, video);
            });
            return false;
            return;
        }
        this.videoElement = videoElement;

    }

    initPlyrInstance() {
        // Уже инициализирован — выходим
        if (this.player) {
            return;
        }

        const videoElement = this.videoElement;

        // Создаём экземпляр Plyr
        this.player = new Plyr(this.domElements.videoElement, {
            controls: [
                'play-large',
                'play',
                'progress',
                'current-time',
                'duration',
                'mute',
                'volume',
                'settings',
                'pip',
                'fullscreen'
            ],
            hideControls: true,
            seekTime: 10
        });


        console.log('✅ Plyr инициализирован');

        // Теперь можно загрузить первое видео
        this.loadFirstVideo();

        // Устанавливаем флаг
        this.hasInitialized = true;

        // Обработчик ошибок
        this.player.on('error', (event) => {
            console.error('❌ Ошибка Plyr:', event.detail?.error || event);
        });
    }

    bindEvents() {
        // Кнопки управления контейнером
        this.domElements.togglePlayerBtn.addEventListener('click', () => this.minimize());
        this.domElements.togglePlaylistBtn.addEventListener('click', () => this.togglePlaylist());
        this.domElements.closePlayerBtn.addEventListener('click', () => this.hide());

        // Обработчики для элементов плейлиста
        this.domElements.playlistItems.forEach(item => {
            item.addEventListener('click', (e) => {
                this.loadVideoFromPlaylist(item);
            });
        });

        // Закрытие по клику вне области (опционально)
        document.addEventListener('click', (e) => {
            if (!this.domElements.container.contains(e.target) &&
                !e.target.closest('[data-toggle-player]')) {
                this.minimize();
            }
        });

        const minimized = this.domElements.container.querySelector('.video-player-minimized');
        const togglePlayerBtn = this.domElements.togglePlayerBtn;
        const closePlayerBtn = this.domElements.closePlayerBtn;

        // Открыть по клику на мини-кнопку
        if (minimized) {
            minimized.addEventListener('click', () => this.expand());
        }

        // Сворачивание/разворачивание (иконка)
        // if (togglePlayerBtn) {
        //     togglePlayerBtn.addEventListener('click', () => this.toggleMinimize());
        // }

        // Закрыть
        if (closePlayerBtn) {
            closePlayerBtn.addEventListener('click', () => this.closeModal());
        }

        // Закрыть по клику на оверлей
        const overlay = document.getElementById('video-modal-overlay');
        overlay?.addEventListener('click', () => this.closeModal());

        // Обработчики плейлиста
        this.domElements.playlistItems.forEach(item => {
            item.addEventListener('click', () => this.loadVideoFromPlaylist(item));
        });
    }

    loadFirstVideo() {
        if (this.hasLoadedFirstVideo) {
            return;
        }

        if (this.domElements.playlistItems.length > 0) {
            this.loadVideoFromPlaylist(this.domElements.playlistItems[0]);
            this.hasLoadedFirstVideo = true;
        }
    }


    loadVideoFromPlaylist(playlistItem) {
        const newSrc = playlistItem.dataset.videoSrc.trim();

        // Не перезагружать то же самое видео
        if (this.currentVideo && this.currentVideo.src === newSrc) {
            return;
        }


        // Убираем активный класс со всех элементов
        this.domElements.playlistItems.forEach(item => {
            item.classList.remove('active');
        });

        // Добавляем активный класс к текущему элементу
        playlistItem.classList.add('active');

        // Получаем данные видео
        this.currentVideo = {
            src: encodeURI(playlistItem.dataset.videoSrc),
            poster: playlistItem.dataset.posterSrc || '', // Добавляем fallback
            title: playlistItem.dataset.videoTitle
        };

        console.log('Загружаем видео:', this.currentVideo);

        // Обновляем интерфейс
        this.domElements.nowPlayingTitle.textContent = this.currentVideo.title;

        // Загружаем видео в плеер через официальный API
        if (this.player && this.player.media) {
            // Устанавливаем источник
            this.player.source = {
                type: 'video',
                title: this.currentVideo.title,
                sources: [
                    {
                        src: this.currentVideo.src,
                        type: 'video/mp4'
                    }
                ],
                poster: this.currentVideo.poster
            };

            // Воспроизводим после загрузки метаданных
            this.player.once('loadedmetadata', () => {
                this.player.play().catch(error => {
                    console.error('Ошибка воспроизведения:', error);
                });
            });
        } else {
            console.error('Plyr не инициализирован');
        }
    }

    toggleMinimize() {
        this.isMinimized ? this.expand() : this.minimize();
    }

    minimize() {
        this.domElements.container.classList.add('minimized');
        this.isMinimized = true;
        this.domElements.togglePlayerBtn.querySelector('i').className = 'fa fa-window-maximize';
    }

    expand() {
        this.isMinimized = false;

        // Показываем развёрнутое состояние
        this.domElements.container.querySelector('.video-player-minimized').style.display = 'none';
        this.domElements.container.querySelector('.video-player-expanded').classList.remove('d-none');

        // Ждём, пока элемент станет видимым, и инициализируем Plyr
        // Убедимся, что размеры доступны
        setTimeout(() => {
            this.initPlyrInstance();
        }, 10);

        this.expandModal();
    }

    togglePlaylist() {
        this.isPlaylistVisible = !this.isPlaylistVisible;
        this.domElements.container.classList.toggle('playlist-hidden', !this.isPlaylistVisible);

        const icon = this.domElements.togglePlaylistBtn.querySelector('i');
        icon.className = this.isPlaylistVisible ? 'fa fa-list' : 'fa fa-list-ul';
    }

    close() {
        if (this.player) {
            this.player.destroy();
        }
        this.domElements.container.remove();
    }

    hide(){
        this.domElements.container.classList.add('hidden');
        this.isHidden = true;
    }

    show() {
        this.domElements.container.classList.remove('hidden');
        this.isHidden = false;
    }

    // Открыть как модальное окно
    expandModal() {
        this.domElements.container.classList.add('modal-mode');
        document.getElementById('video-modal-overlay').classList.add('show');
        this.isMinimized = false;
    }

    // Закрыть модальное окно
    closeModal() {
        this.domElements.container.classList.remove('modal-mode');
        document.getElementById('video-modal-overlay').classList.remove('show');

        // Остановить видео
        if (this.player && this.player.playing) {
            this.player.pause();
        }

        // Вернуть в свёрнутое состояние
        this.minimize();
    }

    // Минимизировать — вернуться к кнопке
    minimize() {
        this.isMinimized = true;
        this.domElements.container.classList.remove('modal-mode');
        this.domElements.container.querySelector('.video-player-expanded').classList.add('d-none');
        this.domElements.container.querySelector('.video-player-minimized').style.display = 'block';

        if (this.player) {
            this.player.pause();
        }
    }


    // close — закрывает модальное окно
    close() {
        this.closeModal();
        // Можно не удалять — просто скрыть
    }
}

// Глобальная функция для инициализации
function initVideoPlayer(playerId = 'main-video-player') {
    // Проверяем, есть ли контейнер плеера на странице
    if (document.getElementById('video-player-container')) {
        window.videoPlayer = new VideoPlayerManager(playerId);
    }
}

// Автоинициализация при загрузке документа
document.addEventListener('DOMContentLoaded', function () {
    initVideoPlayer();
});

