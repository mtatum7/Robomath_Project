approximationRank15 = score(:,1:15) * coeff(:,1:15)' + repmat(mu, size_occ_m(1), 1);
perfectApprox = score * coeff' + repmat(mu, size_occ_m(1), 1);
approx = approximationRank15;
thresh = 0.2;
s_ar_2 = size(approx);
for i = 1:s_ar_2(1)
    occ = reshape(approx(i,:),[10,10,20]);
    occ(occ < thresh) = 0;
    occ(occ >= thresh) = 1;
    occ = logical(occ);
    [x, y, z] = meshgrid(1:size(occ, 1), 1:size(occ, 2), 1:size(occ, 3));

    x = x(:);
    y = y(:);
    z = z(:);

    ptcloud = pointCloud([x(occ), y(occ), z(occ)]);
    
    hold on;
    pcshow(ptcloud, 'MarkerSize', 1000);
    pcshow([x(~occ), y(~occ), z(~occ)], [1, 0, 0]);
end