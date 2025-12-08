# Translation dictionary
TRANSLATIONS = {
    "en": {
        # --- Common ---
        "welcome_back": "👋 Welcome back, {name}!\n\nI'm ready to work. You can control me using the buttons or by sending voice commands (e.g., 'show clients', 'add new client').",
        "action_cancelled": "Action cancelled.",
        "id_error": "ID Error",
        "list_empty": "📂 The list is empty.",
        "db_empty": "❌ Database is empty.",
        "generation_error": "❌ Generation error.",
        "command_not_recognized": "❓ Command not recognized. Please try again.",
        "btn_back": "🔙 Back",
        "btn_cancel": "❌ Cancel",
        "btn_confirm": "✅ Confirm",
        "btn_today": "Today",
        "btn_tomorrow": "Tomorrow",
        "btn_prev": "⬅️ Prev",
        "btn_next": "Next ➡️",
        "processing_request": "⏳ Processing your request...",

        # --- Auth ---
        "auth_required": "🔒 <b>Access restricted.</b>\nPlease enter the administrator password:",
        "auth_success": "🔓 <b>Access granted!</b>\nWelcome to the system.\n\nYou can control me using the buttons or by sending voice commands (e.g., 'show clients', 'add new client').",
        "auth_failed": "⛔ <b>Invalid password.</b> Please try again:",

        # --- Main Menu ---
        "btn_clients": "👥 Clients",
        "btn_add": "➕ Add Client",
        "btn_schedule": "📅 Schedule",
        "btn_settings": "⚙️ Settings",
        "btn_stats": "📊 Statistics",

        # --- Clients ---
        "client_menu_title": "📂 Client Menu",
        "btn_show_all": "🗂 Show All",
        "btn_search_by_name": "🔍 Search by Name",
        "btn_filter_by_status": "📊 Filter by Status",
        "ask_search_query": "Please enter a name to search for:",
        "search_results_title": "🔍 Search Results",
        "search_no_results": "No clients found matching your query.",
        "add_client_name": "📝 <b>New client.</b>\nEnter name:",
        "enter_name_text": "Please enter a name using text.",
        "add_client_phone": "📞 Enter <b>Phone number</b> (or send a dot '.' if none):",
        "add_client_notes": "🗒 Write a <b>Note</b> about the client.\n🎤 <i>You can send a voice message, and I will transcribe it!</i>",
        "send_text_or_voice": "Please send text or a voice message.",
        "client_created_success": "✅ <b>Client successfully created!</b>\n👤 Name: {name}\n📝 Note: {notes}",
        "db_save_error": "❌ Error saving to DB: {error}",
        "client_list_empty": "📂 Client list is empty.",
        "client_list_select": "📂 <b>Select a client to view:</b>",
        "client_list_select_update": "📂 <b>Select a client to update:</b>",
        "client_list_select_call": "📂 <b>Select a client to create a call for:</b>",
        "select_client": "📂 <b>Select a client:</b>",
        "client_not_found": "❌ Client not found (perhaps deleted).",
        "client_card_template": "👤 <b>{name}</b>\n➖➖➖➖➖➖➖➖\n📱 Phone: {phone}\n🏷 Status: {status}\n📝 <b>Note:</b>\n{notes}",
        "client_deleted": "🗑 Client deleted",
        "btn_export_excel": "📉 Download full database (Excel)",
        "generating_excel": "⏳ Generating Excel file...",
        "excel_caption": "📉 <b>Full client database</b>",
        "btn_create_call": "📞 Create call",
        "btn_export_pdf": "📄 Download dossier (PDF)",
        "generating_pdf": "⏳ Generating PDF...",
        "pdf_caption": "📄 <b>Client dossier</b>",
        "btn_delete": "🗑 Delete",
        "btn_back_to_list": "🔙 Back to list",
        "btn_change_status": "🔄 Change Status",
        "btn_history": "📜 History",
        "select_status": "Please select the new status for the client:",
        "status_changed": "✅ Status for client {name} has been changed to {status}.",
        "client_history_title": "📜 Client History: {name}",
        "no_history": "No history yet.",


        # --- Calls ---
        "select_call_date": "📅 <b>Select the call date:</b>",
        "select_call_hour": "📅 Date: <b>{date}</b>\n🕓 Select the hour (in your time):",
        "select_call_minute": "📅 Date: <b>{date}</b>\n🕓 Time: <b>{time}</b> (specify minutes):",
        "ask_call_topic": "✅ Time selected: <b>{dt}</b>\n\n📌 <b>Write the call topic</b> (or send a voice message):",
        "call_no_topic": "Call (No topic)",
        "call_created": "✅ Call scheduled for {msk_time} MSK ({paris_time} Paris)",
        "ics_caption": "📅 <i>Click the file to add the meeting to your phone's calendar</i>",
        "btn_mark_done": "✅ Mark as Done",
        "btn_cancel_call": "❌ Cancel Call",
        "btn_edit_notes": "📝 Edit Notes",
        "btn_no_changes": "👍 No Changes",
        "call_follow_up": "How did the call with {client_name} go? Any updates?",
        "call_marked_done": "✅ Call marked as done.",
        "call_cancelled": "❌ Call cancelled.",
        "edit_notes_prompt": "Please send the new notes for the client (text or voice).",
        "notes_updated": "✅ Client notes updated.",
        "btn_add_call_summary": "✍️ Add Call Summary",
        "add_call_summary_prompt": "Please send a summary for the call with {client_name} (text or voice).",
        "call_summary_added": "✅ Call summary added.",

        # --- Schedule ---
        "schedule_title": "📅 <b>Schedule ({period})</b>\n\n",
        "schedule_empty": "🌴 No plans for this week.",
        "daily_summary_title": "📅 <b>Daily Summary</b>",
        "todays_calls_title": "Calls for Today:",
        "overdue_calls_title": "🔥 Overdue Calls:",
        "call_reminder": "🔔 <b>REMINDER!</b>\nIn {minutes} minutes, you have a call with: <b>{client_name}</b>\n📞 Phone: {client_phone}\n📌 Topic: {topic}",

        # --- Settings ---
        "settings_title": "⚙️ <b>Settings</b>\nYour language: {lang}\nYour timezone: {tz}\nReminder delay: {delay} minutes",
        "choose_lang": "Choose language:",
        "lang_set": "✅ Language set to English",
        "choose_tz": "🌍 Select your timezone:",
        "tz_set": "✅ Timezone set to: {tz}",
        "btn_change_lang": "🗣 Language",
        "btn_change_tz": "🌍 Timezone",
        "btn_change_reminder": "⏰ Reminder Time",
        "ask_reminder_time": "Please enter the new reminder time in minutes (e.g., 15):",
        "reminder_time_set": "✅ Reminder time set to {minutes} minutes.",
        "invalid_reminder_time": "❌ Invalid input. Please enter a number.",


        # --- Statistics ---
        "stats_menu_title": "📊 Statistics",
        "btn_stats_week": "Report for this week",
        "btn_stats_month": "Report for this month",
        "stats_report_title": "📈 Statistics for {period}",
        "stats_new_clients": "New clients",
        "stats_calls_made": "Calls scheduled",
        "stats_to_deposit": "Converted to 'Deposit'",
        "stats_to_dead": "Converted to 'Dead'",


        # --- Voice & AI ---
        "voice_listen": "🎤 Listening ({lang})...",
        "voice_processing": "🎧 Listening and transcribing...",
        "voice_error": "⚠️ Error processing voice: {error}",
        "audio_error_placeholder": "[Audio error]",
        "voice_recognized": "🗣: <i>{text}</i>",
        "ai_thinking": "🤖 I understood: \"<i>{text}</i>\". Analyzing the command...",
        "ai_missing_data": "⚠️ I understood the command, but couldn't extract all the necessary information (like client name or date). Please try again.",
        "ai_confirmation_prompt_new_client": "❓ <b>Confirm Action</b>\n\nCreate <b>new</b> client <b>{client_name}</b> and schedule a call for <b>{date}</b>?\n- Topic: <i>{topic}</i>",
        "ai_confirmation_prompt_existing_client": "❓ <b>Confirm Action</b>\n\nSchedule a call for existing client <b>{client_name}</b> on <b>{date}</b>?\n- Topic: <i>{topic}</i>",
        "ai_client_and_call_created": "✅ Done! Created client <b>{client_name}</b> and scheduled a call for <b>{msk_time} MSK ({paris_time} Paris)</b>.\nTopic: {topic}.",
        "ai_call_created_for_existing_client": "✅ Done! Scheduled a call for <b>{client_name}</b> for <b>{msk_time} MSK ({paris_time} Paris)</b>.\nTopic: {topic}.",
        "ai_execution_error": "❌ An error occurred while executing the command: {error}",
    },
    "fr": {
        # --- Common ---
        "welcome_back": "👋 Bon retour, {name}!\n\nJe suis prêt à travailler. Vous pouvez me contrôler via les boutons ou en envoyant des commandes vocales (par ex. 'afficher les clients', 'ajouter un nouveau client').",
        "action_cancelled": "Action annulée.",
        "id_error": "Erreur d'ID",
        "list_empty": "📂 La liste est vide.",
        "db_empty": "❌ La base de données est vide.",
        "generation_error": "❌ Erreur de génération.",
        "command_not_recognized": "❓ Commande non reconnue. Veuillez réessayer.",
        "btn_back": "🔙 Retour",
        "btn_cancel": "❌ Annuler",
        "btn_confirm": "✅ Confirmer",
        "btn_today": "Aujourd'hui",
        "btn_tomorrow": "Demain",
        "btn_prev": "⬅️ Préc.",
        "btn_next": "Suiv. ➡️",
        "processing_request": "⏳ Traitement de votre demande...",

        # --- Auth ---
        "auth_required": "🔒 <b>Accès restreint.</b>\nVeuillez entrer le mot de passe administrateur :",
        "auth_success": "🔓 <b>Accès autorisé !</b>\nBienvenue dans le système.\n\nVous pouvez me contrôler via les boutons ou en envoyant des commandes vocales (par ex. 'afficher les clients', 'ajouter un nouveau client').",
        "auth_failed": "⛔ <b>Mot de passe incorrect.</b> Veuillez réessayer :",

        # --- Main Menu ---
        "btn_clients": "👥 Clients",
        "btn_add": "➕ Ajouter",
        "btn_schedule": "📅 Calendrier",
        "btn_settings": "⚙️ Paramètres",
        "btn_stats": "📊 Statistiques",

        # --- Clients ---
        "client_menu_title": "📂 Menu des clients",
        "btn_show_all": "🗂 Tout afficher",
        "btn_search_by_name": "🔍 Rechercher par nom",
        "btn_filter_by_status": "📊 Filtrer par statut",
        "ask_search_query": "Veuillez entrer un nom à rechercher :",
        "search_results_title": "🔍 Résultats de la recherche",
        "search_no_results": "Aucun client ne correspond à votre recherche.",
        "add_client_name": "📝 <b>Nouveau client.</b>\nEntrez le nom :",
        "enter_name_text": "Veuillez entrer un nom texte.",
        "add_client_phone": "📞 Entrez le <b>numéro de téléphone</b> (ou envoyez un point '.' si aucun) :",
        "add_client_notes": "🗒 Rédigez une <b>note</b> sur le client.\n🎤 <i>Vous pouvez envoyer un message vocal, et je le transcrirai !</i>",
        "send_text_or_voice": "Veuillez envoyer un texte ou un message vocal.",
        "client_created_success": "✅ <b>Client créé avec succès !</b>\n👤 Nom : {name}\n📝 Note : {notes}",
        "db_save_error": "❌ Erreur lors de la sauvegarde en BDD : {error}",
        "client_list_empty": "📂 La liste de clients est vide.",
        "client_list_select": "📂 <b>Sélectionnez un client à afficher :</b>",
        "client_list_select_update": "📂 <b>Sélectionnez un client à mettre à jour :</b>",
        "client_list_select_call": "📂 <b>Sélectionnez un client pour créer un appel :</b>",
        "select_client": "📂 <b>Sélectionnez un client :</b>",
        "client_not_found": "❌ Client non trouvé (peut-être supprimé).",
        "client_card_template": "👤 <b>{name}</b>\n➖➖➖➖➖➖➖➖\n📱 Téléphone : {phone}\n🏷 Statut: {status}\n📝 <b>Note :</b>\n{notes}",
        "client_deleted": "🗑 Client supprimé",
        "btn_export_excel": "📉 Télécharger la base complète (Excel)",
        "generating_excel": "⏳ Génération du fichier Excel...",
        "excel_caption": "📉 <b>Base de clients complète</b>",
        "btn_create_call": "📞 Créer un appel",
        "btn_export_pdf": "📄 Télécharger le dossier (PDF)",
        "generating_pdf": "⏳ Génération du PDF...",
        "pdf_caption": "📄 <b>Dossier client</b>",
        "btn_delete": "🗑 Supprimer",
        "btn_back_to_list": "🔙 Retour à la liste",
        "btn_change_status": "🔄 Changer le statut",
        "btn_history": "📜 Historique",
        "select_status": "Veuillez sélectionner le nouveau statut pour le client :",
        "status_changed": "✅ Le statut du client {name} a été changé en {status}.",
        "client_history_title": "📜 Historique du client : {name}",
        "no_history": "Aucun historique pour le moment.",

        # --- Calls ---
        "select_call_date": "📅 <b>Sélectionnez la date de l'appel :</b>",
        "select_call_hour": "📅 Date : <b>{date}</b>\n🕓 Sélectionnez l'heure (votre heure) :",
        "select_call_minute": "📅 Date : <b>{date}</b>\n🕓 Heure : <b>{time}</b> (précisez les minutes) :",
        "ask_call_topic": "✅ Heure sélectionnée : <b>{dt}</b>\n\n📌 <b>Écrivez le sujet de l'appel</b> (ou envoyez un message vocal) :",
        "call_no_topic": "Appel (Sans sujet)",
        "call_created": "✅ Appel prévu pour {msk_time} MSK ({paris_time} Paris)",
        "ics_caption": "📅 <i>Cliquez sur le fichier pour ajouter la réunion à votre calendrier</i>",
        "btn_mark_done": "✅ Marquer comme terminé",
        "btn_cancel_call": "❌ Annuler l'appel",
        "btn_edit_notes": "📝 Modifier les notes",
        "btn_no_changes": "👍 Pas de changements",
        "call_follow_up": "Comment s'est passé l'appel avec {client_name} ? Des mises à jour ?",
        "call_marked_done": "✅ Appel marqué comme terminé.",
        "call_cancelled": "❌ Appel annulé.",
        "edit_notes_prompt": "Veuillez envoyer les nouvelles notes pour le client (texte ou vocal).",
        "notes_updated": "✅ Notes du client mises à jour.",
        "btn_add_call_summary": "✍️ Ajouter un résumé",
        "add_call_summary_prompt": "Veuillez envoyer un résumé pour l'appel avec {client_name} (texte ou vocal).",
        "call_summary_added": "✅ Résumé de l'appel ajouté.",

        # --- Schedule ---
        "schedule_title": "📅 <b>Planning ({period})</b>\n\n",
        "schedule_empty": "🌴 Aucun plan pour cette semaine.",
        "daily_summary_title": "📅 <b>Résumé du jour</b>",
        "todays_calls_title": "Appels du jour :",
        "overdue_calls_title": "🔥 Appels en retard :",
        "call_reminder": "🔔 <b>RAPPEL !</b>\nDans {minutes} minutes, appel avec : <b>{client_name}</b>\n📌 Sujet : {topic}",

        # --- Settings ---
        "settings_title": "⚙️ <b>Paramètres</b>\nVotre langue : {lang}\nVotre fuseau horaire : {tz}\nDélai de rappel : {delay} minutes",
        "choose_lang": "Choisissez la langue :",
        "lang_set": "✅ Langue définie sur le Français",
        "choose_tz": "🌍 Choisissez votre fuseau horaire :",
        "tz_set": "✅ Fuseau horaire défini : {tz}",
        "btn_change_lang": "🗣 Langue",
        "btn_change_tz": "🌍 Fuseau horaire",
        "btn_change_reminder": "⏰ Délai de rappel",
        "ask_reminder_time": "Veuillez entrer le nouveau délai de rappel en minutes (par ex. 15) :",
        "reminder_time_set": "✅ Délai de rappel défini à {minutes} minutes.",
        "invalid_reminder_time": "❌ Entrée invalide. Veuillez entrer un nombre.",

        # --- Statistics ---
        "stats_menu_title": "📊 Statistiques",
        "btn_stats_week": "Rapport de la semaine",
        "btn_stats_month": "Rapport du mois",
        "stats_report_title": "📈 Statistiques pour {period}",
        "stats_new_clients": "Nouveaux clients",
        "stats_calls_made": "Appels planifiés",
        "stats_to_deposit": "Convertis en 'Deposit'",
        "stats_to_dead": "Convertis en 'Dead'",

        # --- Voice & AI ---
        "voice_listen": "🎤 J'écoute ({lang})...",
        "voice_processing": "🎧 Écoute et transcription...",
        "voice_error": "⚠️ Erreur de traitement vocal : {error}",
        "audio_error_placeholder": "[Erreur audio]",
        "voice_recognized": "🗣: <i>{text}</i>",
        "ai_thinking": "🤖 J'ai compris : \"<i>{text}</i>\". Analyse de la commande...",
        "ai_missing_data": "⚠️ J'ai compris la commande, mais je n'ai pas pu extraire toutes les informations nécessaires (comme le nom du client ou la date). Veuillez réessayer.",
        "ai_confirmation_prompt_new_client": "❓ <b>Confirmer l'action</b>\n\nCréer un <b>nouveau</b> client <b>{client_name}</b> et planifier un appel pour le <b>{date}</b> ?\n- Sujet : <i>{topic}</i>",
        "ai_confirmation_prompt_existing_client": "❓ <b>Confirmer l'action</b>\n\nPlanifier un appel pour le client existant <b>{client_name}</b> le <b>{date}</b> ?\n- Sujet : <i>{topic}</i>",
        "ai_client_and_call_created": "✅ C'est fait ! Client <b>{client_name}</b> créé et un appel programmé pour le <b>{msk_time} MSK ({paris_time} Paris)</b>.\nSujet : {topic}.",
        "ai_call_created_for_existing_client": "✅ C'est fait ! Appel programmé pour <b>{client_name}</b> le <b>{msk_time} MSK ({paris_time} Paris)</b>.\nSujet : {topic}.",
        "ai_execution_error": "❌ Une erreur est survenue lors de l'exécution de la commande : {error}",
    }
}

def t(key: str, lang: str = "en", **kwargs) -> str:
    """Get a translation."""
    # Get the dictionary for the desired language, falling back to 'en'
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    # Get the text by key, using the key itself as a fallback for debugging
    text = lang_dict.get(key, key)
    
    # Add the language itself to the formatting variables, if needed in the text
    kwargs['lang'] = lang
    
    # Format the string, replacing placeholders like {name} with values
    return text.format(**kwargs)

def all_t(key: str) -> list[str]:
    """Returns a list of all translations for a single key."""
    return [
        TRANSLATIONS[lang].get(key, key) 
        for lang in TRANSLATIONS
    ]