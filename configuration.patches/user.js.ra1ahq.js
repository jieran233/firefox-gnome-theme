/*** https://ra1ahq.blog/en/optimizaciya-proizvoditelnosti-mozilla-firefox ***/

user_pref("javascript.options.baselinejit.threshold", 50);
user_pref("javascript.options.ion.threshold", 5000);
user_pref("network.buffer.cache.size", 65535);

user_pref("javascript.options.concurrent_multiprocess_gcs.cpu_divisor", 8);

user_pref("browser.display.auto_quality_min_font_size", 0);  // 0 for modern PCs and 4k monitors, 1000 for weak computers
