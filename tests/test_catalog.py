from streamflix.catalog import RealVideo, ProxyVideo


def test_proxy_does_not_load_real_video_until_played():
    ProxyVideo("Inception", "/videos/inception.mp4")

    assert RealVideo.load_count == 0


def test_proxy_loads_real_video_on_first_play():
    proxy = ProxyVideo("Inception", "/videos/inception.mp4")

    result = proxy.play()

    assert result == "Playing 'Inception' from /videos/inception.mp4"
    assert RealVideo.load_count == 1


def test_proxy_reuses_real_video_on_later_plays():
    proxy = ProxyVideo("Inception", "/videos/inception.mp4")

    for _ in range(3):
        assert proxy.play() == "Playing 'Inception' from /videos/inception.mp4"

    assert RealVideo.load_count == 1


def test_independent_proxies_load_independent_real_videos():
    proxy_a = ProxyVideo("Inception", "/videos/inception.mp4")
    proxy_b = ProxyVideo("Interstellar", "/videos/interstellar.mp4")

    proxy_a.play()
    proxy_b.play()

    assert RealVideo.load_count == 2
