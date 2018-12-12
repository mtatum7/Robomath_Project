clear;
close;

load('generated/gen_0999.mat');
% volumes = upsample(volumes);

[x, y, z] = meshgrid(1:size(volumes, 1), 1:size(volumes, 2), 1:size(volumes, 3));

x = x(:);
y = y(:);
z = z(:);

volumes(volumes > 1) = 1;
volumes(volumes < 0) = 0;

colormap(flipud(parula));
sizedata = volumes(:) * 100;
sizedata(sizedata == 0) = NaN;
scatter3(x, y, z, 'SizeData', sizedata, 'MarkerFaceColor', 'flat', 'MarkerEdgeColor', 'k', 'CData', volumes(:));
axis 'equal'

% pc = pointCloud([x, y, z], 'Intensity', volumes(:));
% pcshow(pc, 'MarkerSize', 1000);