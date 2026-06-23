package id.ac.rti.api.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

/**
 * Dokumen MongoDB yang memetakan kolom IKEA_product_catalog.csv.
 * @JsonProperty memastikan JSON request/response pakai snake_case,
 * konsisten dengan payload k6 dan model .NET.
 */
@Document(collection = "ikea_products")
public class Product {

    @Id
    private String id;

    @Indexed(unique = true)
    @Field("unique_id")
    @JsonProperty("unique_id")
    private String uniqueId;

    @Field("product_id")
    @JsonProperty("product_id")
    private String productId;

    @Field("product_name")
    @JsonProperty("product_name")
    private String productName;

    @Field("product_type")
    @JsonProperty("product_type")
    private String productType;

    @Field("product_measurements")
    @JsonProperty("product_measurements")
    private String productMeasurements;

    @Field("product_description")
    @JsonProperty("product_description")
    private String productDescription;

    @Field("main_category")
    @JsonProperty("main_category")
    private String mainCategory;

    @Field("sub_category")
    @JsonProperty("sub_category")
    private String subCategory;

    @Field("product_rating")
    @JsonProperty("product_rating")
    private Double productRating;

    @Field("product_rating_count")
    @JsonProperty("product_rating_count")
    private Double productRatingCount;

    @Field("badge")
    private String badge;

    @Field("online_sellable")
    @JsonProperty("online_sellable")
    private String onlineSellable;

    @Field("url")
    private String url;

    @Field("price")
    private Double price;

    @Field("currency")
    private String currency;

    @Field("discount")
    private String discount;

    @Field("sale_tag")
    @JsonProperty("sale_tag")
    private String saleTag;

    @Field("country")
    private String country;

    // --- constructors ---

    public Product() {}

    // --- getters & setters ---

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getUniqueId() { return uniqueId; }
    public void setUniqueId(String uniqueId) { this.uniqueId = uniqueId; }

    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }

    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }

    public String getProductType() { return productType; }
    public void setProductType(String productType) { this.productType = productType; }

    public String getProductMeasurements() { return productMeasurements; }
    public void setProductMeasurements(String productMeasurements) { this.productMeasurements = productMeasurements; }

    public String getProductDescription() { return productDescription; }
    public void setProductDescription(String productDescription) { this.productDescription = productDescription; }

    public String getMainCategory() { return mainCategory; }
    public void setMainCategory(String mainCategory) { this.mainCategory = mainCategory; }

    public String getSubCategory() { return subCategory; }
    public void setSubCategory(String subCategory) { this.subCategory = subCategory; }

    public Double getProductRating() { return productRating; }
    public void setProductRating(Double productRating) { this.productRating = productRating; }

    public Double getProductRatingCount() { return productRatingCount; }
    public void setProductRatingCount(Double productRatingCount) { this.productRatingCount = productRatingCount; }

    public String getBadge() { return badge; }
    public void setBadge(String badge) { this.badge = badge; }

    public String getOnlineSellable() { return onlineSellable; }
    public void setOnlineSellable(String onlineSellable) { this.onlineSellable = onlineSellable; }

    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }

    public Double getPrice() { return price; }
    public void setPrice(Double price) { this.price = price; }

    public String getCurrency() { return currency; }
    public void setCurrency(String currency) { this.currency = currency; }

    public String getDiscount() { return discount; }
    public void setDiscount(String discount) { this.discount = discount; }

    public String getSaleTag() { return saleTag; }
    public void setSaleTag(String saleTag) { this.saleTag = saleTag; }

    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
}
