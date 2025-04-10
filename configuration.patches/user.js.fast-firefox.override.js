/*** Override for fast-firefox ***/
user_pref("dom.ipc.processCount", 8);
user_pref("dom.ipc.processCount.webIsolated", 4);

user_pref("dom.ipc.processPriorityManager.backgroundUsesEcoQoS", false);  // Disabling Efficiency Mode (for Windows 11)

/*** Disable WebRender due to bug in some hardware ***/
user_pref("gfx.webrender.all", false);
user_pref("gfx.webrender.compositor", false);
user_pref("gfx.webrender.compositor.force-enabled", false);
user_pref("gfx.webrender.enabled", false);
user_pref("gfx.webrender.precache-shaders", false);
user_pref("gfx.webrender.program-binary-disk", false);
user_pref("gfx.webrender.software.opengl", false);