# Mismo producto y versión que la evaluación local. Imagen oficial verificada.
FROM sissbruecker/linkding:1.47.0@sha256:e35cb50e0581178f245125ffaa909c565416c94c9f22ace305a7d234a4345522

ENV DJANGO_SETTINGS_MODULE=bookmarks.settings.prod
COPY deploy/render_settings.py /etc/linkding/bookmarks/settings/custom.py
COPY deploy/start-render.sh /etc/linkding/deploy/start-render.sh
RUN chmod 755 /etc/linkding/deploy/start-render.sh
EXPOSE 10000
CMD ["/etc/linkding/deploy/start-render.sh"]
