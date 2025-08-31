// Файл: static/js/_video_player.js

class VideoPlayerManager {
    constructor(playerId = 'main-player') {
        this.playerId = playerId;
        this.player = null;
        this.currentVideo = null;
        this.isMinimized = false;
        this.isPlaylistVisible = true;
        this.domElements = {};

        this.init();
    }

    init() {
        this.cacheDomElements();
        this.initPlyr();
        this.bindEvents();
        // this.loadFirstVideo();
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
        const videoElement = this.domElements.videoElement;

        if (!videoElement) {
            console.error('Video element not found!');
            return;
        }

        // Инициализируем Plyr на нашем video-элементе
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

        // События Plyr
        this.player.on('ready', () => {
            console.log('Plyr готов к работе');
            this.loadFirstVideo();
        });

        this.player.on('error', (error) => {
        console.error('Ошибка Plyr:', error);
    });
    }

    bindEvents() {
        // Кнопки управления контейнером
        this.domElements.togglePlayerBtn.addEventListener('click', () => this.toggleMinimize());
        this.domElements.togglePlaylistBtn.addEventListener('click', () => this.togglePlaylist());
        this.domElements.closePlayerBtn.addEventListener('click', () => this.close());

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
    }

    loadFirstVideo() {
        if (this.domElements.playlistItems.length > 0) {
            this.loadVideoFromPlaylist(this.domElements.playlistItems[0]);
        }
    }


    loadVideoFromPlaylist(playlistItem) {
    // Убираем активный класс со всех элементов
    this.domElements.playlistItems.forEach(item => {
        item.classList.remove('active');
    });

    // Добавляем активный класс к текущему элементу
    playlistItem.classList.add('active');

    // Получаем данные видео
    this.currentVideo = {
        src: playlistItem.dataset.videoSrc,
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
            this.domElements.togglePlayerBtn.querySelector('i').className = 'fas fa-window-maximize';
        }

        expand() {
            this.domElements.container.classList.remove('minimized');
            this.isMinimized = false;
            this.domElements.togglePlayerBtn.querySelector('i').className = 'fas fa-window-minimize';
        }

        togglePlaylist() {
            this.isPlaylistVisible = !this.isPlaylistVisible;
            this.domElements.container.classList.toggle('playlist-hidden', !this.isPlaylistVisible);

            const icon = this.domElements.togglePlaylistBtn.querySelector('i');
            icon.className = this.isPlaylistVisible ? 'fas fa-list' : 'fas fa-list-ul';
        }

        close() {
            if (this.player) {
                this.player.destroy();
            }
            this.domElements.container.remove();
        }
}

// Глобальная функция для инициализации
function initVideoPlayer(playerId = 'main-player') {
    // Проверяем, есть ли контейнер плеера на странице
    if (document.getElementById('video-player-container')) {
        window.videoPlayer = new VideoPlayerManager(playerId);
    }
}

// Автоинициализация при загрузке документа
document.addEventListener('DOMContentLoaded', function() {
    initVideoPlayer();
});