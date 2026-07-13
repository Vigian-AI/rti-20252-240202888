using DotnetApi.Models;
using MongoDB.Driver;

namespace DotnetApi.Services;

/// <summary>
/// Service layer untuk operasi CRUD pada koleksi ikea_products.
/// Dipisah dari controller agar mapping variabel riset tetap jelas:
/// service = komponen yang berinteraksi dengan DV (data layer).
/// </summary>
public class ProductService
{
    private readonly IMongoCollection<Product> _collection;

    public ProductService(IConfiguration config)
    {
        var connectionString = Environment.GetEnvironmentVariable("MONGO_URI")
            ?? config["MongoDB:ConnectionString"]
            ?? "mongodb://localhost:27017";

        var database = Environment.GetEnvironmentVariable("MONGO_DB")
            ?? config["MongoDB:Database"]
            ?? "benchmark_db";

        var collectionName = config["MongoDB:Collection"] ?? "ikea_products";

        var client = new MongoClient(connectionString);
        var db = client.GetDatabase(database);
        _collection = db.GetCollection<Product>(collectionName);
    }

    public async Task<List<Product>> GetAllAsync(int page = 0, int size = 20) =>
        await _collection.Find(_ => true)
            .Skip(page * size)
            .Limit(size)
            .ToListAsync();

    public async Task<Product?> GetByIdAsync(string id) =>
        await _collection.Find(p => p.Id == id).FirstOrDefaultAsync();

    public async Task<Product> CreateAsync(Product product)
    {
        await _collection.InsertOneAsync(product);
        return product;
    }

    public async Task<bool> UpdateAsync(string id, Product updated)
    {
        updated.Id = id;
        var result = await _collection.ReplaceOneAsync(p => p.Id == id, updated);
        return result.ModifiedCount > 0;
    }

    public async Task<bool> DeleteAsync(string id)
    {
        var result = await _collection.DeleteOneAsync(p => p.Id == id);
        return result.DeletedCount > 0;
    }
}
