export default function PropertyCard({ listing }) {
  const domainUrl = listing.listing_slug
    ? `https://www.domain.com.au/${listing.listing_slug}`
    : null;

  return (
    <div className="property-card">
      {listing.image_url ? (
        <img
          className="property-image"
          src={listing.image_url}
          alt={listing.headline || "Property"}
          loading="lazy"
        />
      ) : (
        <div className="property-image placeholder">No image</div>
      )}

      <div className="property-info">
        <div className="property-price">{listing.price_display || "Price on request"}</div>
        <div className="property-address">{listing.address}</div>
        <h3 className="property-headline">{listing.headline}</h3>

        <div className="property-features">
          {listing.bedrooms != null && (
            <span title="Bedrooms">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 7v11a2 2 0 002 2h14a2 2 0 002-2V7" />
                <path d="M3 14h18" />
                <path d="M6 7V4h12v3" />
              </svg>
              {listing.bedrooms}
            </span>
          )}
          {listing.bathrooms != null && (
            <span title="Bathrooms">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M4 12h16a1 1 0 011 1v3a4 4 0 01-4 4H7a4 4 0 01-4-4v-3a1 1 0 011-1z" />
                <path d="M6 12V5a2 2 0 012-2h1" />
              </svg>
              {listing.bathrooms}
            </span>
          )}
          {listing.carspaces != null && (
            <span title="Car spaces">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="1" y="6" width="22" height="12" rx="2" />
                <path d="M5 18v2M19 18v2M5 6l2-4h10l2 4" />
              </svg>
              {listing.carspaces}
            </span>
          )}
          {listing.property_type && (
            <span className="property-type-badge">{listing.property_type}</span>
          )}
        </div>

        {domainUrl && (
          <a
            className="property-link"
            href={domainUrl}
            target="_blank"
            rel="noopener noreferrer"
          >
            View on Domain
          </a>
        )}
      </div>
    </div>
  );
}
