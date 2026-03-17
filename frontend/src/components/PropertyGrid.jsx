import PropertyCard from "./PropertyCard";

export default function PropertyGrid({ listings }) {
  return (
    <div className="property-grid">
      {listings.map((listing) => (
        <PropertyCard key={listing.id} listing={listing} />
      ))}
    </div>
  );
}
