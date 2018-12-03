%[coeff, score, latent, tsquared, explained, mu] = pca(occ_matrix);
%size_occ_m = size(occ_matrix);
reconstructed = score * coeff' + repmat(mu, size_occ_m(1),1);
error = zeros([1,size_occ_m(1)]);
for i = 1:size_occ_m(1)-1
    approximationRank = score(:,1:i) * coeff(:,1:i)' + repmat(mu, size_occ_m(1), 1);
    error(i) = sum(sum((occ_matrix - approximationRank).^2));
end
plot(1:1000,error)