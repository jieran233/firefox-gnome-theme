/*** Override for fast-firefox ***/

/* Revert processCount options*/
// user_pref("dom.ipc.processCount", 8);
user_pref("dom.ipc.processCount", 16);  // depends on user's system (nproc, ram)
user_pref("dom.ipc.processCount.webIsolated", 4);

/* Revert disabling network separations */
user_pref("fission.autostart", false);
user_pref("privacy.partition.network_state", false);

// Disabling Efficiency Mode (for Windows 11)
user_pref("dom.ipc.processPriorityManager.backgroundUsesEcoQoS", false);

// Enabling Fork Server (for Linux)
user_pref("dom.ipc.forkserver.enable", true);

/*** Disable WebRender due to bug in some hardware ***/
/* Please note that some features such as WebGPU and WebRender support are still 
experimental, the specifications are not fully implemented in Firefox yet, and
may cause stability issues in some hardware configurations under Linux. */
user_pref("gfx.webrender.all", false);
user_pref("gfx.webrender.compositor", false);
user_pref("gfx.webrender.compositor.force-enabled", false);
user_pref("gfx.webrender.enabled", false);
user_pref("gfx.webrender.precache-shaders", false);
user_pref("gfx.webrender.program-binary-disk", false);
user_pref("gfx.webrender.software.opengl", false);