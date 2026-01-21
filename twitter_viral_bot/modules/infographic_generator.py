"""
Infographic generator - Creates engaging visuals from data
"""
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Optional
import io
import textwrap
from ..config import Config


class InfographicGenerator:
    """Generates infographics and visual content for tweets"""

    def __init__(self):
        self.output_dir = Config.OUTPUT_DIR
        self.default_size = (1200, 675)  # Twitter optimized 16:9
        self.colors = {
            "primary": "#1DA1F2",  # Twitter blue
            "secondary": "#14171A",
            "accent": "#657786",
            "background": "#FFFFFF",
            "text": "#14171A"
        }

    def create_stat_card(
        self,
        main_stat: str,
        context: str,
        subtitle: Optional[str] = None,
        output_name: str = "stat_card.png"
    ) -> Path:
        """
        Create a clean stat card with a big number/percentage

        Args:
            main_stat: The main statistic (e.g., "85%", "$1.2B")
            context: Context for the stat
            subtitle: Optional subtitle
            output_name: Output filename

        Returns:
            Path to generated image
        """
        img = Image.new('RGB', self.default_size, color=self.colors["background"])
        draw = ImageDraw.Draw(img)

        # Try to load a nice font, fallback to default
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
            context_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            context_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Draw main stat centered
        bbox = draw.textbbox((0, 0), main_stat, font=title_font)
        stat_width = bbox[2] - bbox[0]
        stat_height = bbox[3] - bbox[1]
        stat_x = (self.default_size[0] - stat_width) // 2
        stat_y = 180

        draw.text((stat_x, stat_y), main_stat, fill=self.colors["primary"], font=title_font)

        # Draw context text
        wrapped_context = textwrap.fill(context, width=40)
        bbox = draw.textbbox((0, 0), wrapped_context, font=context_font)
        context_width = bbox[2] - bbox[0]
        context_x = (self.default_size[0] - context_width) // 2
        context_y = stat_y + stat_height + 40

        draw.text((context_x, context_y), wrapped_context, fill=self.colors["text"], font=context_font, align="center")

        # Draw subtitle if provided
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = bbox[2] - bbox[0]
            subtitle_x = (self.default_size[0] - subtitle_width) // 2
            subtitle_y = context_y + 120

            draw.text((subtitle_x, subtitle_y), subtitle, fill=self.colors["accent"], font=subtitle_font)

        # Add subtle accent line
        draw.rectangle([100, 100, self.default_size[0] - 100, 105], fill=self.colors["primary"])

        # Save
        output_path = self.output_dir / output_name
        img.save(output_path, quality=95)

        return output_path

    def create_key_points_graphic(
        self,
        title: str,
        points: List[str],
        output_name: str = "key_points.png"
    ) -> Path:
        """
        Create a graphic with key points/tips

        Args:
            title: Title of the graphic
            points: List of key points (max 5)
            output_name: Output filename

        Returns:
            Path to generated image
        """
        img = Image.new('RGB', self.default_size, color=self.colors["background"])
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
            point_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
            number_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        except:
            title_font = ImageFont.load_default()
            point_font = ImageFont.load_default()
            number_font = ImageFont.load_default()

        # Draw title
        wrapped_title = textwrap.fill(title, width=35)
        draw.text((80, 60), wrapped_title, fill=self.colors["text"], font=title_font)

        # Draw points
        y_offset = 180
        for i, point in enumerate(points[:5], 1):
            # Draw number circle
            circle_x = 80
            circle_y = y_offset
            circle_radius = 30
            draw.ellipse(
                [circle_x, circle_y, circle_x + 2*circle_radius, circle_y + 2*circle_radius],
                fill=self.colors["primary"]
            )
            draw.text((circle_x + 15, circle_y + 5), str(i), fill="white", font=number_font)

            # Draw point text
            wrapped_point = textwrap.fill(point, width=40)
            draw.text((circle_x + 80, circle_y + 5), wrapped_point, fill=self.colors["text"], font=point_font)

            y_offset += 100

        # Save
        output_path = self.output_dir / output_name
        img.save(output_path, quality=95)

        return output_path

    def create_comparison_chart(
        self,
        labels: List[str],
        values: List[float],
        title: str,
        output_name: str = "comparison.png"
    ) -> Path:
        """
        Create a comparison bar chart

        Args:
            labels: Labels for each bar
            values: Values for each bar
            title: Chart title
            output_name: Output filename

        Returns:
            Path to generated image
        """
        plt.figure(figsize=(12, 6.75), facecolor='white')
        sns.set_style("whitegrid")

        # Create bar chart
        colors = [self.colors["primary"], self.colors["accent"], self.colors["secondary"]]
        bars = plt.barh(labels, values, color=colors[:len(labels)])

        # Styling
        plt.title(title, fontsize=24, fontweight='bold', pad=20)
        plt.xlabel('')
        plt.ylabel('')
        plt.tight_layout()

        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2,
                    f' {values[i]:.1f}',
                    ha='left', va='center', fontsize=16, fontweight='bold')

        # Save
        output_path = self.output_dir / output_name
        plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def create_quote_card(
        self,
        quote: str,
        attribution: str,
        output_name: str = "quote.png"
    ) -> Path:
        """
        Create a quote card graphic

        Args:
            quote: The quote text
            attribution: Who said it
            output_name: Output filename

        Returns:
            Path to generated image
        """
        img = Image.new('RGB', self.default_size, color=self.colors["background"])
        draw = ImageDraw.Draw(img)

        try:
            quote_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf", 48)
            attr_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            quote_font = ImageFont.load_default()
            attr_font = ImageFont.load_default()

        # Draw large quotation mark
        draw.text((100, 100), '"', fill=self.colors["primary"], font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 200))

        # Draw quote
        wrapped_quote = textwrap.fill(quote, width=35)
        draw.text((100, 280), wrapped_quote, fill=self.colors["text"], font=quote_font)

        # Draw attribution
        draw.text((100, 520), f"— {attribution}", fill=self.colors["accent"], font=attr_font)

        # Save
        output_path = self.output_dir / output_name
        img.save(output_path, quality=95)

        return output_path

    def create_from_research(self, research_data: Dict) -> List[Path]:
        """
        Auto-generate relevant infographics from research data

        Args:
            research_data: Research data from ResearchEngine

        Returns:
            List of paths to generated images
        """
        generated_images = []

        # Create stat cards for statistics
        if "statistics" in research_data and research_data["statistics"]:
            for i, stat_data in enumerate(research_data["statistics"][:3]):
                try:
                    path = self.create_stat_card(
                        main_stat=stat_data.get("stat", ""),
                        context=stat_data.get("context", ""),
                        output_name=f"stat_{i+1}.png"
                    )
                    generated_images.append(path)
                except Exception as e:
                    print(f"Failed to create stat card {i+1}: {e}")

        # Create key points graphic
        if "key_points" in research_data and research_data["key_points"]:
            try:
                points = [kp.get("point", "") for kp in research_data["key_points"][:5]]
                path = self.create_key_points_graphic(
                    title=research_data.get("main_topic", "Key Insights"),
                    points=points,
                    output_name="key_points.png"
                )
                generated_images.append(path)
            except Exception as e:
                print(f"Failed to create key points graphic: {e}")

        # Create quote card for expert insights
        if "expert_insights" in research_data and research_data["expert_insights"]:
            try:
                insight = research_data["expert_insights"][0]
                path = self.create_quote_card(
                    quote=insight.get("insight", ""),
                    attribution=insight.get("attribution", "Expert"),
                    output_name="quote.png"
                )
                generated_images.append(path)
            except Exception as e:
                print(f"Failed to create quote card: {e}")

        return generated_images
