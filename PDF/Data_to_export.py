#phase 1

import requests
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from fpdf import FPDF
import os

class Trading212API:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": f"{self.api_key}"}
        self.base_url = "https://demo.trading212.com/api/v0/"

    def fetch_portfolio_data(self):
        url = self.base_url + "equity/portfolio"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print("Fetched portfolio data successfully!")
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Failed to fetch portfolio data: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return []

    def process_portfolio_data(self, portfolio_data):
        processed_data = []
        for item in portfolio_data:
            processed_data.append({
                "Ticker": item.get("ticker"),
                "Quantity": item.get("quantity"),
                "Average Price": item.get("averagePrice"),
                "Current Price": item.get("currentPrice"),
                "PnL": item.get("ppl"),
                "FX PnL": item.get("fxPpl"),
                "Initial Fill Date": item.get("initialFillDate"),
                "Max Buy": item.get("maxBuy"),
                "Max Sell": item.get("maxSell"),
                "Pie Quantity": item.get("pieQuantity")
            })
        return pd.DataFrame(processed_data)

class DataVisualization:
    def __init__(self, portfolio_df):
        self.portfolio_df = portfolio_df

    def portfolio_performance_plotly(self):
        self.portfolio_df["Initial Fill Date"] = pd.to_datetime(self.portfolio_df["Initial Fill Date"], utc=True)
        self.portfolio_df["Stock Value"] = self.portfolio_df["Quantity"] * self.portfolio_df["Current Price"]

        portfolio_value_over_time = self.portfolio_df.groupby("Initial Fill Date")["Stock Value"].sum().sort_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=portfolio_value_over_time.index,
            y=portfolio_value_over_time.values,
            mode="lines+markers",
            name="Portfolio Value"
        ))
        fig.update_layout(
            title="Portfolio Performance Over Time",
            xaxis_title="Date",
            yaxis_title="Portfolio Value (£)",
            template="plotly_white"
        )
        fig.write_image("portfolio_performance_plotly.png", engine="kaleido")
        fig.show()

    def profit_loss_by_investment(self):
        pnl_data = self.portfolio_df[["Ticker", "PnL"]].copy()
        pnl_data = pnl_data.sort_values(by="PnL", ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=pnl_data["Ticker"],
            y=pnl_data["PnL"],
            marker=dict(color=pnl_data["PnL"], colorscale="Viridis"),
            name="P/L"
        ))
        fig.update_layout(
            title="Profit/Loss by Instrument",
            xaxis_title="Instrument (Ticker)",
            yaxis_title="P/L (£)",
            template="plotly_white"
        )
        fig.write_image("profit_loss_by_instrument.png", engine="kaleido")
        fig.show()

    def portfolio_allocation_pie(self):
        self.portfolio_df['Allocation (%)'] = (
            self.portfolio_df['Stock Value'] / self.portfolio_df['Stock Value'].sum() * 100
        )

        threshold = 5
        top_instruments = self.portfolio_df[self.portfolio_df['Allocation (%)'] >= threshold]
        others_allocation = self.portfolio_df[self.portfolio_df['Allocation (%)'] < threshold]['Allocation (%)'].sum()

        if others_allocation > 0:
            others_row = pd.DataFrame([{
                'Ticker': 'Others',
                'Allocation (%)': others_allocation
            }])
            top_instruments = pd.concat([top_instruments, others_row], ignore_index=True)

        top_instruments = top_instruments.sort_values(by='Allocation (%)', ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=top_instruments['Ticker'],
            values=top_instruments['Allocation (%)'],
            textinfo='percent+label',
            insidetextorientation='radial',
            marker=dict(line=dict(color='#000000', width=1))
        ))
        fig.update_layout(
            title="Portfolio Allocation by Instrument (Top Stocks + Others)",
            title_font_size=22,
            legend_title="Instrument",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            margin=dict(l=50, r=50, t=50, b=100)
        )
        fig.write_image("portfolio_allocation_pie.png", engine="kaleido")
        fig.show()

    def trade_activity_over_time(self):
        self.portfolio_df["Initial Fill Date"] = pd.to_datetime(self.portfolio_df["Initial Fill Date"], utc=True)
        trade_activity = self.portfolio_df.groupby(self.portfolio_df["Initial Fill Date"].dt.date).size()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trade_activity.index,
            y=trade_activity.values,
            mode="lines+markers",
            name="Trades Per Day",
            marker=dict(size=10, color="blue", line=dict(width=2, color="black")),
            line=dict(width=2)
        ))
        fig.update_layout(
            title="Trade Activity Over Time",
            title_font_size=22,
            xaxis_title="Date",
            yaxis_title="Number of Trades",
            template="plotly_white",
            xaxis=dict(showgrid=True, tickangle=45),
            yaxis=dict(showgrid=True),
            margin=dict(l=50, r=50, t=50, b=100)
        )
        fig.write_image("trade_activity_over_time.png", engine="kaleido")
        fig.show()

    def pnl_breakdown(self):


        self.portfolio_df["PnL Category"] = self.portfolio_df["PnL"].apply(
            lambda x: "Positive PnL" if x >= 0 else "Negative PnL"
        )
        pnl_breakdown = self.portfolio_df.groupby("PnL Category")["PnL"].sum()


        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=pnl_breakdown.index,
            y=pnl_breakdown.values,
            marker=dict(
                color=["green" if pnl > 0 else "red" for pnl in pnl_breakdown.values],
                line=dict(color="black", width=1.5)
            ),
            text=[f"{val:.2f}" for val in pnl_breakdown.values],
            textposition="outside",
            name="PnL Breakdown"
        ))


        fig.update_layout(
            title="PnL Breakdown by Category",
            title_font_size=22,
            xaxis_title="PnL Category",
            yaxis_title="PnL (£)",
            template="plotly_white",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            margin=dict(l=50, r=50, t=50, b=100),
            legend=dict(
                title="Legend",
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )


        fig.show()
        fig.write_image("pnl_breakdown.png", engine="kaleido")


class PortfolioPDF:
    def __init__(self, output_file="Portfolio_Report.pdf"):
        self.output_file = output_file
        self.pdf = FPDF(orientation='P', unit='mm', format='A4')
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.set_font("Arial", size=12)

    def add_title_page(self, title="BlackElm Equity Portfolio Report", subtitle="In-depth Portfolio Analysis"):
        self.pdf.add_page()

        #change logo_path if running locally
        logo_path = "/Users/mansur/Downloads/blackelmequity_logo.jpeg"
        if os.path.exists(logo_path):
            self.pdf.image(logo_path, x=80, y=10, w=50)
        else:
            print("Logo not found! Ensure the logo file is in the working directory.")

        self.pdf.ln(60)
        self.pdf.set_font("Arial", style="B", size=24)
        self.pdf.cell(0, 10, title, ln=True, align="C")

        self.pdf.set_font("Arial", style="", size=14)
        self.pdf.ln(10)
        self.pdf.cell(0, 10, subtitle, ln=True, align="C")

        self.pdf.ln(10)
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 10, "Date: 2024-11-27", ln=True, align="C")

    def add_section_title(self, title):
        self.pdf.set_font("Arial", style="B", size=16)
        self.pdf.ln(10)
        self.pdf.cell(0, 10, title, ln=True)

    def add_text(self, text):
        self.pdf.set_font("Arial", size=12)
        self.pdf.multi_cell(0, 10, text)

    def add_table(self, dataframe, title):
        self.add_section_title(title)
        self.pdf.set_font("Arial", size=10)
        self.pdf.ln(5)

        col_width = self.pdf.w / len(dataframe.columns) - 10
        for col_name in dataframe.columns:
            self.pdf.cell(col_width, 10, str(col_name), border=1, align="C")
        self.pdf.ln()

        for _, row in dataframe.iterrows():
            for col_name in dataframe.columns:
                self.pdf.cell(col_width, 10, str(row[col_name]), border=1)
            self.pdf.ln()

    def add_chart(self, chart_path, title):
        self.add_section_title(title)
        if os.path.exists(chart_path):
            self.pdf.image(chart_path, x=10, y=None, w=190)
            self.pdf.ln(85)  # Adjust based on image height for each image etc
        else:
            self.add_text(f"Chart not found: {chart_path}")

    def save_pdf(self):
        self.pdf.output(self.output_file)
        print(f"PDF saved as {self.output_file}")





if __name__ == "__main__":
    api_key = "20155216ZpCEwlxRBQEXFJzupJKWZkYRIQWnu"
    trading_api = Trading212API(api_key)

    portfolio_data = trading_api.fetch_portfolio_data()
    portfolio_df = trading_api.process_portfolio_data(portfolio_data)

    if portfolio_df.empty:
        print("No portfolio data found!")
    else:
        print("Processed Portfolio Data:")
        print(portfolio_df)

        portfolio_df["Stock Name"] = portfolio_df["Ticker"]

        visualization = DataVisualization(portfolio_df)
        visualization.portfolio_performance_plotly()
        visualization.profit_loss_by_investment()
        visualization.portfolio_allocation_pie()
        visualization.trade_activity_over_time()
        visualization.pnl_breakdown()

    pdf_generator = PortfolioPDF()


    pdf_generator.add_title_page()


    pdf_generator.add_text(
        "This report provides an in-depth analysis of BlackElm Equity Portfolio, including performance trends, PnL breakdown, and trade activity insights.")


    sample_df = portfolio_df[["Ticker", "Quantity", "PnL", "Current Price"]]
    pdf_generator.add_table(sample_df, "Portfolio Overview")

    pdf_generator.add_chart("portfolio_performance_plotly.png", "Portfolio Performance Over Time")
    pdf_generator.add_chart("profit_loss_by_instrument.png", "Profit/Loss by Instrument")
    pdf_generator.add_chart("portfolio_allocation_pie.png", "Portfolio Allocation by Instrument")
    pdf_generator.add_chart("trade_activity_over_time.png", "Trade Activity Over Time")
    pdf_generator.add_chart("pnl_breakdown.png", "PnL Breakdown by Category")


    pdf_generator.save_pdf()




