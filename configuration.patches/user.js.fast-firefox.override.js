/*** Override for fast-firefox ***/
user_pref("dom.ipc.processCount", 8);
user_pref("dom.ipc.processCount.webIsolated", 4);

user_pref("dom.ipc.processPriorityManager.backgroundUsesEcoQoS", false);  // Disabling Efficiency Mode (for Windows 11)