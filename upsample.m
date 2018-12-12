function upsampled = upsample(sample_points)
        
    step1 = upsample_x(sample_points);
    step2 = upsample_y(step1);
    step3 = upsample_z(step2);
    upsampled = step3;
end

function upsampled = upsample_x(sample_points)
    axis = [1, 0, 0];
    zeros_size = size(sample_points) .* (axis + 1) - axis;
    upsampled = zeros(zeros_size);
    
    for i = 1:size(upsampled, 1)
        if mod(i, 2) == 1
            orig = (i+1)/2;
            upsampled(i, :, :) = sample_points(orig, :, :); % Direct copy
        else
            orig1 = i/2;
            orig2 = orig1 + 1;
            upsampled(i, :, :) = (sample_points(orig1, :, :) + sample_points(orig2, :, :)) / 2;
        end
    end
end

function upsampled = upsample_y(sample_points)
    axis = [0, 1, 0];
    zeros_size = size(sample_points) .* (axis + 1) - axis;
    upsampled = zeros(zeros_size);
    
    for i = 1:size(upsampled, 2)
        if mod(i, 2) == 1
            orig = (i+1)/2;
            upsampled(:, i, :) = sample_points(:, orig, :); % Direct copy
        else
            orig1 = i/2;
            orig2 = orig1 + 1;
            upsampled(:, i, :) = (sample_points(:, orig1, :) + sample_points(:, orig2, :)) / 2;
        end
    end
end

function upsampled = upsample_z(sample_points)
    axis = [0, 0, 1];
    zeros_size = size(sample_points) .* (axis + 1) - axis;
    upsampled = zeros(zeros_size);
    
    for i = 1:size(upsampled, 3)
        if mod(i, 2) == 1
            orig = (i+1)/2;
            upsampled(:, :, i) = sample_points(:, :, orig); % Direct copy
        else
            orig1 = i/2;
            orig2 = orig1 + 1;
            upsampled(:, :, i) = (sample_points(:, :, orig1) + sample_points(:, :, orig2)) / 2;
        end
    end
end