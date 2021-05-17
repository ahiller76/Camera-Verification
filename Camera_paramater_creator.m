clear File;

File = fopen('CameraParams.txt', 'w');

fprintf(File, '%s\r\n', '# Camera Intrinsics');

fprintf(File, '%s\r\n', '# Principal Point');
fprintf(File, '%f %f\r\n',cameraParams.Intrinsics.PrincipalPoint);

fprintf(File, '%s\r\n', '# Number of Images');
fprintf(File, '%f %f\r\n',cameraParams.NumPatterns);

fprintf(File, '\n %s\r\n', '# K');
for i = 1:size(cameraParams.IntrinsicMatrix,1)
    fprintf(File, '%f %f %f\r\n', cameraParams.IntrinsicMatrix(i,:));
end

fprintf(File, '%s\r\n', '# Camera Extrinsics');
fprintf(File, '%s\r\n', '# RotationMatrices');

for i = 1:size(cameraParams.RotationMatrices, 3)
    fprintf(File, '# RotationMatrix %d\r\n', i);
    for j = 1:size(cameraParams.RotationMatrices, 2)
        fprintf(File, '%f %f %f\r\n', cameraParams.RotationMatrices(j,:,i));
    end
end

fprintf(File, '%s\r\n', '# TranslationVectors');
for i = 1:size(cameraParams.TranslationVectors, 1)
    fprintf(File, '# TranslationVector %d\r\n', i);
    fprintf(File, '%f\r\n%f\r\n%f\r\n', cameraParams.TranslationVectors(i,:));
end

fclose(File);