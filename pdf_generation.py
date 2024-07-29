from fpdf import FPDF
from datetime import datetime
import os


class PDF(FPDF):
    def header(self):
        pass  # No header on the title page

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(255, 255, 255)  # White
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title, chapter_id):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)  # White
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_link(chapter_id, y=-1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.set_text_color(255, 255, 255)  # White
        self.multi_cell(0, 10, body)
        self.ln()

    def add_summary_text(self, summary, title, chapter_id):
        self.add_page()
        self.set_fill_color(33, 33, 33)  # Carbon grey background
        self.rect(0, 0, self.w, self.h, 'F')
        self.set_link(chapter_id)
        self.set_font("Arial", size=16, style='B')
        self.set_text_color(255, 255, 255)  # White
        self.cell(0, 10, title, ln=True)
        self.ln(10)
        self.set_font("Arial", size=12)
        for idx, row in summary.iterrows():
            row_text = f"{idx}: " + ", ".join([f"{col}: {val:.2f}" for col, val in row.items()])
            self.multi_cell(0, 10, row_text)
            self.ln(2)


def generate_pdf(category, summary_sum, summary_avg, links, performance_links, output_directory):
    try:
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add title page
        pdf.add_page()
        pdf.set_fill_color(33, 33, 33)  # Carbon grey background
        pdf.rect(0, 0, pdf.w, pdf.h, 'F')

        # Title at the top
        pdf.set_y(30)
        pdf.set_font("Arial", size=30, style='B')
        pdf.set_text_color(255, 255, 255)  # White
        pdf.cell(0, 10, f"{category} Monthly Report", ln=True, align='C')

        # Logo in the middle
        logo_width = 100
        logo_height = 100
        pdf.set_y(70)
        pdf.image('Logo.png', x=(pdf.w - logo_width) / 2, w=logo_width, h=logo_height)

        # Subtitle with name and channel below the logo
        pdf.set_y(180)
        pdf.set_font("Arial", size=24, style='B')
        pdf.cell(0, 10, "Channel Name", ln=True, align='C')

        pdf.set_font("Arial", size=16)
        pdf.cell(0, 10, "by Kostas Tziortzis", ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 20, f"Report Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')

        # Add content page
        pdf.add_page()
        pdf.set_fill_color(33, 33, 33)  # Carbon grey background
        pdf.rect(0, 0, pdf.w, pdf.h, 'F')
        pdf.set_font("Arial", size=16, style='B')
        pdf.set_text_color(255, 255, 255)  # White
        pdf.cell(0, 10, "Contents", ln=True)
        pdf.set_font("Arial", size=12)
        summed_link = pdf.add_link()
        pdf.cell(0, 10, "Summary of Summed Metrics", ln=True, link=summed_link)

        # Add entries for total metrics graphs
        content_links = []
        for title, _ in links:
            link = pdf.add_link()
            content_links.append(link)
            pdf.cell(0, 10, title, ln=True, link=link)

        # Add entries for performance metrics graphs
        performance_content_links = []
        for perf_title, _ in performance_links:
            perf_link = pdf.add_link()
            performance_content_links.append(perf_link)
            pdf.cell(0, 10, perf_title, ln=True, link=perf_link)

        # Add summary for summed metrics
        pdf.add_summary_text(summary_sum, "Summary of Summed Metrics", summed_link)

        # Add graphs with titles
        for (title, total_graph), (perf_title, perf_graph), link, perf_link in zip(links, performance_links,
                                                                                   content_links,
                                                                                   performance_content_links):
            if total_graph and perf_graph:  # Ensure graphs are not empty
                pdf.add_page()
                pdf.set_fill_color(33, 33, 33)  # Carbon grey background
                pdf.rect(0, 0, pdf.w, pdf.h, 'F')
                pdf.chapter_title(title, link)
                pdf.image(total_graph, x=10, y=30, w=190)
                pdf.ln(150)  # Adjust spacing between the graphs
                pdf.chapter_title(perf_title, perf_link)
                pdf.image(perf_graph, x=10, y=150, w=190)

        file_name = f"{category}_Monthly_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(os.path.join(output_directory, file_name))
    except Exception as e:
        print(f"Error generating PDF for {category}: {e}")
