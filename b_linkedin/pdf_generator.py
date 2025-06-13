from fpdf import FPDF
from PIL import Image
import requests
from io import BytesIO

class CampaignPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "LinkedIn Content Campaign Report", ln=True, align="C")
        self.ln(5)

    def add_post(self, post_number, post_text, visual_concept, overlay_instructions, image_url=None):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Post {post_number}", ln=True)
        self.set_font("Arial", "", 11)

        self.multi_cell(0, 8, f"Post Text:\n{post_text}")
        self.ln(1)
        self.multi_cell(0, 8, f"Visual Concept:\n{visual_concept}")
        self.ln(1)
        self.multi_cell(0, 8, f"Text Overlay Instructions:\n{overlay_instructions}")
        self.ln(2)

        if image_url:
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img.thumbnail((500, 280))
                img_path = f"temp_post_{post_number}.jpg"
                img.save(img_path, format="JPEG")
                self.image(img_path, w=170)
                self.ln(5)
            except Exception as e:
                self.multi_cell(0, 8, f"(Failed to load image: {e})")


def generate_campaign_pdf(posts_data):
    pdf = CampaignPDF()
    pdf.add_page()

    for idx, post in enumerate(posts_data, start=1):
        pdf.add_post(
            post_number=idx,
            post_text=post['post_text'],
            visual_concept=post['visual_concept'],
            overlay_instructions=post['overlay_instructions'],
            image_url=post.get('image_url')
        )

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output
