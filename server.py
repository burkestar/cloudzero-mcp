from typing import Dict, List, Optional
import httpx
from pydantic import BaseModel, Field
from mcp.server.fastmcp import Context, FastMCP
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

# Load environment variables
load_dotenv()

class CostQuery(BaseModel):
    start_date: Optional[str] = Field(None, description="Start date for cost query")
    end_date: Optional[str] = Field(None, description="End date for cost query")

class CloudZeroAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cloudzero.com/v2"
        self.client = httpx.AsyncClient()
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        response = await self.client.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data,
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

@dataclass
class AppContext:
    api: CloudZeroAPI

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Server lifespan context manager"""
    # Initialize API client
    api = CloudZeroAPI(api_key=os.getenv("CLOUDZERO_API_KEY", ""))

    try:
        # Test connection
        await api.make_request("GET", "billing/dimensions")
        yield AppContext(api=api)
    finally:
        # Cleanup
        if api:
            await api.close()


mcp = FastMCP("CloudZero", dependencies=[], lifespan=app_lifespan)

@mcp.tool()
async def get_costs(ctx: Context, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    """Get billing costs for a specified date range"""
    api = ctx.request_context.lifespan_context.api
    if not api:
        raise RuntimeError("CloudZero API client not initialized")
    params = {"start_date": start_date, "end_date": end_date}
    return await api.make_request("GET", "billing/costs", params=params)

@mcp.tool()
async def get_dimensions(ctx: Context) -> Dict:
    """Get billing dimensions"""
    api = ctx.request_context.lifespan_context.api
    if not api:
        raise RuntimeError("CloudZero API client not initialized")
    return await api.make_request("GET", "billing/dimensions")

@mcp.tool()
async def list_budgets(ctx: Context) -> List[Dict]:
    """List all budgets"""
    api = ctx.request_context.lifespan_context.api
    if not api:
        raise RuntimeError("CloudZero API client not initialized")
    return await api.make_request("GET", "budgets")

@mcp.tool()
async def list_insights(ctx: Context) -> List[Dict]:
    """List all insights"""
    api = ctx.request_context.lifespan_context.api
    if not api:
        raise RuntimeError("CloudZero API client not initialized")
    return await api.make_request("GET", "insights")

@mcp.prompt()
async def analyze_costs(ctx: Context, period: str) -> str:
    """Create a cost analysis prompt for a specific period"""
    return f"""Please analyze the costs for {period} and provide insights on:
1. Overall spending patterns
2. Major cost centers
3. Potential cost optimization opportunities
4. Budget compliance"""
