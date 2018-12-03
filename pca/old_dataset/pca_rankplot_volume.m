file_list = dir('mats/mats');
occ_matrix = zeros([29, 1500]); %[observations, variables]
for i = 3:length(file_list)
    file_dest = sprintf('mats/mats/%s',file_list(i).name);
    load(file_dest);
    occ = volumes;
    occ = occ(:,:,1:15);
    occ_vec = reshape(occ, [1,prod(size(occ))]);
    occ_matrix(i-2,:) = occ_vec;
end
[coeff, score, latent, tsquared, explained, mu] = pca(occ_matrix);
explained;
size_occ_m = size(occ_matrix);
reconstructed = score * coeff' + repmat(mu, size_occ_m(1),1);
error = zeros([1,size_occ_m(1)]);
for i = 1:size_occ_m(1)-1
    approximationRank = score(:,1:i) * coeff(:,1:i)' + repmat(mu, size_occ_m(1), 1);
    error(i) = sum(sum((occ_matrix - approximationRank).^2));
end
plot(1:29,error)