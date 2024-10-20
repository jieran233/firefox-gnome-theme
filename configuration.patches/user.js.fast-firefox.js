/****************************************************************************
 * fast_firefox
 * Author: RubenKelevra
 * url: https://gist.github.com/RubenKelevra/fd66c2f856d703260ecdf0379c4f59db
****************************************************************************/

// General tweaks
user_pref("network.captive-portal-service.enabled", false);
user_pref("network.notify.checkForProxies", false);

// Browser cache
user_pref("browser.cache.disk.capacity", 8192000);
user_pref("browser.cache.disk.smart_size.enabled", false);
user_pref("browser.cache.frecency_half_life_hours", 18);
user_pref("browser.cache.max_shutdown_io_lag", 16);
user_pref("browser.cache.memory.capacity", 2097152);
user_pref("browser.cache.memory.max_entry_size", 327680);
user_pref("browser.cache.disk.metadata_memory_limit", 15360);

// GFX rendering tweaks
user_pref("gfx.canvas.accelerated", true);
user_pref("gfx.canvas.accelerated.cache-items", 32768);
user_pref("gfx.canvas.accelerated.cache-size", 4096);
user_pref("layers.acceleration.force-enabled", false);
user_pref("gfx.content.skia-font-cache-size", 80);
user_pref("gfx.webrender.all", true);
user_pref("gfx.webrender.compositor", true);
user_pref("gfx.webrender.compositor.force-enabled", true);
user_pref("gfx.webrender.enabled", true);
user_pref("gfx.webrender.precache-shaders", true);
user_pref("gfx.webrender.program-binary-disk", true);
user_pref("gfx.webrender.software.opengl", true);
user_pref("image.mem.decode_bytes_at_a_time", 65536);
user_pref("image.mem.shared.unmap.min_expiration_ms", 120000);
user_pref("layers.gpu-process.enabled", true);
user_pref("layers.gpu-process.force-enabled", true);
user_pref("image.cache.size", 10485760);
user_pref("media.memory_cache_max_size", 1048576);
user_pref("media.memory_caches_combined_limit_kb", 3145728);
user_pref("media.hardware-video-decoding.force-enabled", true);
user_pref("media.ffmpeg.vaapi.enabled", true);

// Increase predictive network operations
user_pref("network.dns.disablePrefetchFromHTTPS", false);
user_pref("network.dnsCacheEntries", 20000);
user_pref("network.dnsCacheExpiration", 3600);
user_pref("network.dnsCacheExpirationGracePeriod", 240);
user_pref("network.predictor.enable-hover-on-ssl", true);
user_pref("network.predictor.enable-prefetch", true);
user_pref("network.predictor.preconnect-min-confidence", 20);
user_pref("network.predictor.prefetch-force-valid-for", 3600);
user_pref("network.predictor.prefetch-min-confidence", 30);
user_pref("network.predictor.prefetch-rolling-load-count", 120);
user_pref("network.predictor.preresolve-min-confidence", 10);

// Faster SSL
user_pref("network.ssl_tokens_cache_capacity", 32768);

// Disable network separations
user_pref("fission.autostart", false);
user_pref("privacy.partition.network_state", false);

// Reduce the number of processes
user_pref("dom.ipc.processCount", 1);
user_pref("dom.ipc.processCount.webIsolated", 1);