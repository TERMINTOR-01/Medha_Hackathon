from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class Patient(models.Model):
    # Patient Basic Info
    name = models.CharField(max_length=100, verbose_name="Patient Name")
    p_id = models.CharField(max_length=10, unique=True, verbose_name="Patient ID (e.g., P-101)")
    age = models.IntegerField()
    diagnosis=models.CharField(max_length=255, default="Not Specified")
    admission_date = models.DateField(auto_now_add=True)
    reviewer_doctor_name = models.CharField(default=False)    
    # Medical Details
    disease = models.CharField(max_length=200, default="Under Observation")
    STATUS_CHOICES = [
        ('Stable', 'Stable'),
        ('Critical', 'Critical'),
        ('ICU', 'ICU'),
        ('Discharged', 'Discharged'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Stable')
    
    # Communication for Relatives
    next_test = models.CharField(max_length=200, help_text="Example: MRI at 4 PM", default="No tests scheduled")
    doctor_note = models.TextField(help_text="Message for relatives in simple language", default="Patient is responding to treatment.")
    plan_of_action = models.TextField(help_text="Doctor's detailed plan of action", default="Continue current treatment and monitor vitals.")
    prcedure_planned = models.TextField(help_text="Planned procedures for the patient", default="No procedures planned.")
    treatment_given=models.TextField(help_text="Details of treatment given to the patient", default="Standard treatment as per diagnosis.")
    next_visit_panned=models.TextField(help_text="Details of next visit planned for the patient", default="Next visit scheduled as per treatment plan.")
    # Auto-Generated QR Code
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Jab bhi save hoga, ye chalega
        # 1. URL Generate karo (Localhost ke liye)
        # Hackathon mein dikhane ke liye hum localhost use kar rahe hain
        url = f"http://127.0.0.1:8000/patient/{self.p_id}/"
        
        # 2. QR Code Image Banao
        qrcode_img = qrcode.make(url)
        qrcode_img = qrcode_img.convert('RGB')
        canvas = Image.new('RGB', (350, 350), 'white')
        
        # Resize QR code to fit in canvas
        qrcode_img_resized = qrcode_img.resize((300, 300))
        
        # Paste QR code at center
        canvas.paste(qrcode_img_resized, (25, 25))
        
        # 3. Image ko Memory mein save karo
        fname = f'qr_code-{self.p_id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        buffer.seek(0)
        
        # 4. Model field mein save karo
        self.qr_code.save(fname, File(buffer), save=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.p_id})"

class Report(models.Model):
    patient = models.ForeignKey('Patient', related_name='reports', on_delete=models.CASCADE)
    file = models.FileField(upload_to='reports/')
    description = models.CharField(max_length=255, blank=True, help_text="Short description of this report")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient.p_id} - {self.file.name.split('/')[-1]}"