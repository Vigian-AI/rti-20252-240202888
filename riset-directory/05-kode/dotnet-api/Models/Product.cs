using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace DotnetApi.Models;

/// <summary>
/// Dokumen MongoDB yang memetakan kolom IKEA_product_catalog.csv.
/// BsonElement memastikan nama field konsisten dengan kolom CSV.
/// BsonIgnoreExtraElements mencegah error jika ada field tak dikenal di dokumen.
/// </summary>
[BsonIgnoreExtraElements]
public class Product
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }

    [BsonElement("unique_id")]
    public string UniqueId { get; set; } = string.Empty;

    [BsonElement("product_id")]
    public string ProductId { get; set; } = string.Empty;

    [BsonElement("product_name")]
    public string ProductName { get; set; } = string.Empty;

    [BsonElement("product_type")]
    public string ProductType { get; set; } = string.Empty;

    [BsonElement("product_measurements")]
    public string ProductMeasurements { get; set; } = string.Empty;

    [BsonElement("product_description")]
    public string ProductDescription { get; set; } = string.Empty;

    [BsonElement("main_category")]
    public string MainCategory { get; set; } = string.Empty;

    [BsonElement("sub_category")]
    public string SubCategory { get; set; } = string.Empty;

    [BsonElement("product_rating")]
    public double? ProductRating { get; set; }

    [BsonElement("product_rating_count")]
    public double? ProductRatingCount { get; set; }

    [BsonElement("badge")]
    public string Badge { get; set; } = string.Empty;

    [BsonElement("online_sellable")]
    public string OnlineSellable { get; set; } = string.Empty;

    [BsonElement("url")]
    public string Url { get; set; } = string.Empty;

    [BsonElement("price")]
    public double? Price { get; set; }

    [BsonElement("currency")]
    public string Currency { get; set; } = string.Empty;

    [BsonElement("discount")]
    public string Discount { get; set; } = string.Empty;

    [BsonElement("sale_tag")]
    public string SaleTag { get; set; } = string.Empty;

    [BsonElement("country")]
    public string Country { get; set; } = string.Empty;
}
