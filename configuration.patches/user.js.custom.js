/************ Custom user.js ************/

// Min width of tabs
user_perf("browser.tabs.tabMinWidth", 128);

// Insert new tab after current
user_perf("browser.tabs.insertAfterCurrent", true);

// Restore pinned tabs on demand
user_perf("browser.sessionstore.restore_on_demand", true);
//user_pref("browser.sessionstore.restore_pinned_tabs_on_demand", true);

// Disable translator popup
user_pref("browser.translations.automaticallyPopup", false);

/********** End custom user.js ***********/