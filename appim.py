import kivy # Kivy kutubxonasini import qilish
from kivy.app import App # Ilovaning asosiy sinfini import qilish
from kivy.uix.label import Label # Matn yozish uchun vidjet
from kivy.uix.button import Button # Tugma yaratish uchun vidjet
from kivy.uix.boxlayout import BoxLayout # Vidjetlarni joylashtirish uchun layout

# Kivy sinfini meros qilib oladigan asosiy ilova sinfimizni yaratamiz
class MeningBirinchiAppim(App):
    # Ilovaning interfeysini (UI) yaratadigan metod
    def build(self):
        # Vidjetlarni vertikal (yuqoridan pastga) joylashtirish uchun layout yaratamiz
        layout = BoxLayout(orientation='vertical')
        
        # 1. Matnni ko'rsatuvchi yorliq (Label) yaratamiz
        salomlashuv_matni = Label(
            text="Salom, APK Dastur!", 
            font_size='30sp' # Shrift hajmi
        )
        
        # 2. Bosish mumkin bo'lgan tugma (Button) yaratamiz
        bosish_tugmasi = Button(
            text="Meni Bos!",
            background_color=(0.1, 0.5, 0.8, 1) # Moviy rang
        )
        
        # 3. Tugmaga bosilganda nima qilishini bog'laymiz
        bosish_tugmasi.bind(on_press=self.tugma_bosildi)
        
        # Vidjetlarni layout ichiga joylashtiramiz
        layout.add_widget(salomlashuv_matni)
        layout.add_widget(bosish_tugmasi)
        
        return layout

    # Tugma bosilganda chaqiriladigan funksiya (qayta aloqa)
    def tugma_bosildi(self, instance):
        print("Tugma bosildi! Qadam tashladingiz.")
        # Bu yerda siz keyinchalik boshqa funksiyalarni qo'shishingiz mumkin
        instance.text = "Bosildi!"


# Ilovani ishga tushirish
if __name__ == '__main__':
    MeningBirinchiAppim().run()