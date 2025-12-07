# Словарь переводов
TRANSLATIONS = {
    "ru": {
        # --- Общие ---
        "welcome_back": "👋 С возвращением, {name}!\nБот готов к работе.",
        "action_cancelled": "Действие отменено.",
        "id_error": "Ошибка ID",
        "list_empty": "📂 Список пуст.",
        "db_empty": "❌ База пуста.",
        "generation_error": "❌ Ошибка генерации.",
        "command_not_recognized": "Команда не распознана.",
        "btn_back": "🔙 Назад",
        "btn_cancel": "❌ Отмена",
        "btn_today": "Сегодня",
        "btn_tomorrow": "Завтра",
        "btn_prev": "⬅️ Пред.",
        "btn_next": "След. ➡️",

        # --- Авторизация ---
        "auth_required": "🔒 <b>Доступ ограничен.</b>\nПожалуйста, введите пароль администратора:",
        "auth_success": "🔓 <b>Доступ разрешен!</b>\nДобро пожаловать в систему.",
        "auth_failed": "⛔ <b>Неверный пароль.</b> Попробуйте еще раз:",

        # --- Главное меню ---
        "btn_clients": "👥 Клиенты",
        "btn_add": "➕ Добавить",
        "btn_schedule": "📅 Расписание",
        "btn_settings": "⚙️ Настройки",

        # --- Клиенты ---
        "add_client_name": "📝 <b>Новый клиент.</b>\nВведите Имя:",
        "enter_name_text": "Пожалуйста, введите имя текстом.",
        "add_client_phone": "📞 Введите <b>Номер телефона</b> (или отправьте точку '.', если нет):",
        "add_client_notes": "🗒 Напишите <b>Заметку</b> о клиенте.\n🎤 <i>Вы можете отправить голосовое сообщение, и я переведу его в текст!</i>",
        "send_text_or_voice": "Пожалуйста, пришлите текст или голосовое.",
        "client_created_success": "✅ <b>Клиент успешно создан!</b>\n👤 Имя: {name}\n📝 Заметка: {notes}",
        "db_save_error": "❌ Ошибка при сохранении в БД: {error}",
        "client_list_empty": "📂 Список клиентов пуст.",
        "client_list_select": "📂 <b>Выберите клиента для просмотра:</b>",
        "select_client": "📂 <b>Выберите клиента:</b>",
        "client_not_found": "❌ Клиент не найден (возможно, удален).",
        "client_card_template": "👤 <b>{name}</b>\n➖➖➖➖➖➖➖➖\n📱 Телефон: {phone}\n🏷 Теги: {tags}\n📝 <b>Заметка:</b>\n{notes}",
        "client_deleted": "🗑 Клиент удален",
        "btn_export_excel": "📉 Скачать всю базу (Excel)",
        "generating_excel": "⏳ Генерирую Excel файл...",
        "excel_caption": "📉 <b>Полная база клиентов</b>",
        "btn_create_call": "📞 Создать созвон",
        "btn_export_pdf": "📄 Скачать досье (PDF)",
        "generating_pdf": "⏳ Генерирую PDF...",
        "pdf_caption": "📄 <b>Досье клиента</b>",
        "btn_delete": "🗑 Удалить",
        "btn_back_to_list": "🔙 Назад к списку",

        # --- Созвоны ---
        "select_call_date": "📅 <b>Выберите дату созвона:</b>",
        "select_call_hour": "📅 Дата: <b>{date}</b>\n🕓 Выберите час (по вашему времени):",
        "select_call_minute": "📅 Дата: <b>{date}</b>\n🕓 Время: <b>{time}</b> (уточните минуты):",
        "ask_call_topic": "✅ Выбрано время: <b>{dt}</b>\n\n📌 <b>Напишите тему созвона</b> (или отправьте голосовое):",
        "call_no_topic": "Созвон (Без темы)",
        "call_created": "✅ Созвон назначен на {date} ({tz})",
        "ics_caption": "📅 <i>Нажмите на файл, чтобы добавить встречу в календарь телефона</i>",

        # --- Расписание ---
        "schedule_title": "📅 <b>Расписание ({period})</b>\n\n",
        "schedule_empty": "🌴 На эту неделю планов нет.",
        "call_reminder": "🔔 <b>НАПОМИНАНИЕ!</b>\nЧерез 10 минут созвон с клиентом: <b>{client_name}</b>\n📌 Тема: {topic}",

        # --- Настройки ---
        "settings_title": "⚙️ <b>Настройки</b>\nВаш язык: {lang}\nВаш пояс: {tz}",
        "choose_lang": "Выберите язык / Choose language / Choisissez la langue:",
        "lang_set": "✅ Язык изменен на Русский",
        "choose_tz": "🌍 Выберите ваш часовой пояс:",
        "tz_set": "✅ Часовой пояс установлен: {tz}",
        "btn_change_lang": "🗣 Language / Язык",
        "btn_change_tz": "🌍 Timezone / Часовой пояс",

        # --- Голос ---
        "voice_listen": "🎤 Слушаю ({lang})...",
        "voice_processing": "🎧 Слушаю и расшифровываю...",
        "voice_error": "⚠️ Ошибка обработки голоса: {error}",
        "audio_error_placeholder": "[Ошибка аудио]",
        "voice_recognized": "🗣: <i>{text}</i>",
    },
    "en": {
        # --- Common ---
        "welcome_back": "👋 Welcome back, {name}!\nThe bot is ready to work.",
        "action_cancelled": "Action cancelled.",
        "id_error": "ID Error",
        "list_empty": "📂 The list is empty.",
        "db_empty": "❌ Database is empty.",
        "generation_error": "❌ Generation error.",
        "command_not_recognized": "Command not recognized.",
        "btn_back": "🔙 Back",
        "btn_cancel": "❌ Cancel",
        "btn_today": "Today",
        "btn_tomorrow": "Tomorrow",
        "btn_prev": "⬅️ Prev",
        "btn_next": "Next ➡️",

        # --- Auth ---
        "auth_required": "🔒 <b>Access restricted.</b>\nPlease enter the administrator password:",
        "auth_success": "🔓 <b>Access granted!</b>\nWelcome to the system.",
        "auth_failed": "⛔ <b>Invalid password.</b> Please try again:",

        # --- Main Menu ---
        "btn_clients": "👥 Clients",
        "btn_add": "➕ Add Client",
        "btn_schedule": "📅 Schedule",
        "btn_settings": "⚙️ Settings",

        # --- Clients ---
        "add_client_name": "📝 <b>New client.</b>\nEnter name:",
        "enter_name_text": "Please enter a name using text.",
        "add_client_phone": "📞 Enter <b>Phone number</b> (or send a dot '.' if none):",
        "add_client_notes": "🗒 Write a <b>Note</b> about the client.\n🎤 <i>You can send a voice message, and I will transcribe it!</i>",
        "send_text_or_voice": "Please send text or a voice message.",
        "client_created_success": "✅ <b>Client successfully created!</b>\n👤 Name: {name}\n📝 Note: {notes}",
        "db_save_error": "❌ Error saving to DB: {error}",
        "client_list_empty": "📂 Client list is empty.",
        "client_list_select": "📂 <b>Select a client to view:</b>",
        "select_client": "📂 <b>Select a client:</b>",
        "client_not_found": "❌ Client not found (perhaps deleted).",
        "client_card_template": "👤 <b>{name}</b>\n➖➖➖➖➖➖➖➖\n📱 Phone: {phone}\n🏷 Tags: {tags}\n📝 <b>Note:</b>\n{notes}",
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

        # --- Calls ---
        "select_call_date": "📅 <b>Select the call date:</b>",
        "select_call_hour": "📅 Date: <b>{date}</b>\n🕓 Select the hour (in your time):",
        "select_call_minute": "📅 Date: <b>{date}</b>\n🕓 Time: <b>{time}</b> (specify minutes):",
        "ask_call_topic": "✅ Time selected: <b>{dt}</b>\n\n📌 <b>Write the call topic</b> (or send a voice message):",
        "call_no_topic": "Call (No topic)",
        "call_created": "✅ Call scheduled for {date} ({tz})",
        "ics_caption": "📅 <i>Click the file to add the meeting to your phone's calendar</i>",

        # --- Schedule ---
        "schedule_title": "📅 <b>Schedule ({period})</b>\n\n",
        "schedule_empty": "🌴 No plans for this week.",
        "call_reminder": "🔔 <b>REMINDER!</b>\nIn 10 minutes, you have a call with: <b>{client_name}</b>\n📌 Topic: {topic}",

        # --- Settings ---
        "settings_title": "⚙️ <b>Settings</b>\nYour language: {lang}\nYour timezone: {tz}",
        "choose_lang": "Choose language:",
        "lang_set": "✅ Language set to English",
        "choose_tz": "🌍 Select your timezone:",
        "tz_set": "✅ Timezone set to: {tz}",
        "btn_change_lang": "🗣 Language",
        "btn_change_tz": "🌍 Timezone",

        # --- Voice ---
        "voice_listen": "🎤 Listening ({lang})...",
        "voice_processing": "🎧 Listening and transcribing...",
        "voice_error": "⚠️ Error processing voice: {error}",
        "audio_error_placeholder": "[Audio error]",
        "voice_recognized": "🗣: <i>{text}</i>",
    },
    "fr": {
        # --- Common ---
        "welcome_back": "👋 Bon retour, {name}!\nLe bot est prêt.",
        "action_cancelled": "Action annulée.",
        "id_error": "Erreur d'ID",
        "list_empty": "📂 La liste est vide.",
        "db_empty": "❌ La base de données est vide.",
        "generation_error": "❌ Erreur de génération.",
        "command_not_recognized": "Commande non reconnue.",
        "btn_back": "🔙 Retour",
        "btn_cancel": "❌ Annuler",
        "btn_today": "Aujourd'hui",
        "btn_tomorrow": "Demain",
        "btn_prev": "⬅️ Préc.",
        "btn_next": "Suiv. ➡️",

        # --- Auth ---
        "auth_required": "🔒 <b>Accès restreint.</b>\nVeuillez entrer le mot de passe administrateur :",
        "auth_success": "🔓 <b>Accès autorisé !</b>\nBienvenue dans le système.",
        "auth_failed": "⛔ <b>Mot de passe incorrect.</b> Veuillez réessayer :",

        # --- Main Menu ---
        "btn_clients": "👥 Clients",
        "btn_add": "➕ Ajouter",
        "btn_schedule": "📅 Calendrier",
        "btn_settings": "⚙️ Paramètres",

        # --- Clients ---
        "add_client_name": "📝 <b>Nouveau client.</b>\nEntrez le nom :",
        "enter_name_text": "Veuillez entrer un nom texte.",
        "add_client_phone": "📞 Entrez le <b>numéro de téléphone</b> (ou envoyez un point '.' si aucun) :",
        "add_client_notes": "🗒 Rédigez une <b>note</b> sur le client.\n🎤 <i>Vous pouvez envoyer un message vocal, et je le transcrirai !</i>",
        "send_text_or_voice": "Veuillez envoyer un texte ou un message vocal.",
        "client_created_success": "✅ <b>Client créé avec succès !</b>\n👤 Nom : {name}\n📝 Note : {notes}",
        "db_save_error": "❌ Erreur lors de la sauvegarde en BDD : {error}",
        "client_list_empty": "📂 La liste de clients est vide.",
        "client_list_select": "📂 <b>Sélectionnez un client à afficher :</b>",
        "select_client": "📂 <b>Sélectionnez un client :</b>",
        "client_not_found": "❌ Client non trouvé (peut-être supprimé).",
        "client_card_template": "👤 <b>{name}</b>\n➖➖➖➖➖➖➖➖\n📱 Téléphone : {phone}\n🏷 Tags : {tags}\n📝 <b>Note :</b>\n{notes}",
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

        # --- Calls ---
        "select_call_date": "📅 <b>Sélectionnez la date de l'appel :</b>",
        "select_call_hour": "📅 Date : <b>{date}</b>\n🕓 Sélectionnez l'heure (votre heure) :",
        "select_call_minute": "📅 Date : <b>{date}</b>\n🕓 Heure : <b>{time}</b> (précisez les minutes) :",
        "ask_call_topic": "✅ Heure sélectionnée : <b>{dt}</b>\n\n📌 <b>Écrivez le sujet de l'appel</b> (ou envoyez un message vocal) :",
        "call_no_topic": "Appel (Sans sujet)",
        "call_created": "✅ Appel prévu pour {date} ({tz})",
        "ics_caption": "📅 <i>Cliquez sur le fichier pour ajouter la réunion à votre calendrier</i>",

        # --- Schedule ---
        "schedule_title": "📅 <b>Planning ({period})</b>\n\n",
        "schedule_empty": "🌴 Aucun plan pour cette semaine.",
        "call_reminder": "🔔 <b>RAPPEL !</b>\nDans 10 minutes, appel avec : <b>{client_name}</b>\n📌 Sujet : {topic}",

        # --- Settings ---
        "settings_title": "⚙️ <b>Paramètres</b>\nVotre langue : {lang}\nVotre fuseau horaire : {tz}",
        "choose_lang": "Choisissez la langue :",
        "lang_set": "✅ Langue définie sur le Français",
        "choose_tz": "🌍 Choisissez votre fuseau horaire :",
        "tz_set": "✅ Fuseau horaire défini : {tz}",
        "btn_change_lang": "🗣 Langue",
        "btn_change_tz": "🌍 Fuseau horaire",

        # --- Voice ---
        "voice_listen": "🎤 J'écoute ({lang})...",
        "voice_processing": "🎧 Écoute et transcription...",
        "voice_error": "⚠️ Erreur de traitement vocal : {error}",
        "audio_error_placeholder": "[Erreur audio]",
        "voice_recognized": "🗣: <i>{text}</i>",
    }
}

def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Функция получения перевода"""
    # Получаем словарь для нужного языка, если его нет - используем 'ru' как запасной
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["ru"])
    
    # Получаем текст по ключу, если его нет - используем ключ как текст (для отладки)
    text = lang_dict.get(key, key)
    
    # Добавляем сам язык в переменные для форматирования, если он нужен в тексте
    kwargs['lang'] = lang
    
    # Форматируем строку, заменяя плейсхолдеры {name} на значения
    return text.format(**kwargs)

def all_t(key: str) -> list[str]:
    """Возвращает список всех переводов для одного ключа."""
    return [
        TRANSLATIONS[lang].get(key, key) 
        for lang in TRANSLATIONS
    ]