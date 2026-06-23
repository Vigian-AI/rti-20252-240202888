using DotnetApi.Models;
using DotnetApi.Services;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);

// ── Services ──────────────────────────────────────────────────────────────────
builder.Services.AddSingleton<ProductService>();

// JSON serializer: gunakan snake_case agar konsisten dengan payload k6 dan Spring Boot
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower;
    options.SerializerOptions.PropertyNameCaseInsensitive = true;
});

var app = builder.Build();

// ── Health check ──────────────────────────────────────────────────────────────
app.MapGet("/health", () => Results.Ok(new { status = "UP" }));

// ── GET all products (paginated) ──────────────────────────────────────────────
app.MapGet("/api/products", async (ProductService service,
    int page = 0, int size = 20) =>
{
    var products = await service.GetAllAsync(page, size);
    return Results.Ok(products);
});

// ── GET product by id ─────────────────────────────────────────────────────────
app.MapGet("/api/products/{id}", async (string id, ProductService service) =>
{
    var product = await service.GetByIdAsync(id);
    return product is not null ? Results.Ok(product) : Results.NotFound();
});

// ── POST create product ───────────────────────────────────────────────────────
app.MapPost("/api/products", async (Product product, ProductService service) =>
{
    var created = await service.CreateAsync(product);
    return Results.Created($"/api/products/{created.Id}", created);
});

// ── PUT update product ────────────────────────────────────────────────────────
app.MapPut("/api/products/{id}", async (string id, Product updated, ProductService service) =>
{
    var success = await service.UpdateAsync(id, updated);
    return success ? Results.Ok(updated) : Results.NotFound();
});

// ── DELETE product ────────────────────────────────────────────────────────────
app.MapDelete("/api/products/{id}", async (string id, ProductService service) =>
{
    var success = await service.DeleteAsync(id);
    return success ? Results.NoContent() : Results.NotFound();
});

app.Run();
