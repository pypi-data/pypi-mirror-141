#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <iostream>
#include <algorithm>

namespace py = pybind11;

using color_t = std::tuple<uint8_t, uint8_t, uint8_t>;


color_t hsl(int r, int g, int b){
    int h,s,l;
    int most, least;
    // This looks stupid, but it's way faster than min() and max().
    if(r > g){
        if(b>r){
            most = b;
            least = g;
        } else if(b > g){
            most = r;
            least = g;
        } else {
            most = r;
            least = b;
        }
    } else {
        if(b > g){
            most = b;
            least = r;
        } else if(b > r){
            most = g;
            least = r;
        } else {
            most = g;
            least = b;
        }
    }

    l = (most + least) >> 1;

    if(most == least){
        h = 0;
        s = 0;
    
    } else {
        int diff = most - least;
        
        if(l > 127){
            s = (int)(diff * 255) / (510 - most - least);
        } else {
            s = (int)(diff * 255) / (most + least);
        }

        if(most == r){
            h = (int)((g - b) * 255) / diff + (g < b ? 1530 : 0);

        } else if(most == g){
            h = (int)((b - r) * 255) / diff + 510;

        } else {
            h = (int)((r - g) * 255) / diff + 1020;
        }
        h /= 6;
    }

    return {h, s, l};
}


std::vector<long> sample(std::vector<color_t>& pixels){
    int top_two_bits = 192; // of 2**8
    int sides = 1 << 2; // Left by the number of bits used.
    std::vector<long> samples(std::pow(sides, 7), 0);

    for(int i=0; i<pixels.size(); i++){
        int r,g,b;
        std::tie(r, g, b) = pixels[i];
        int h,s,l;
        std::tie(h, s, l) = hsl(r, g, b);



        // # Standard constants for converting RGB to relative luminance.
        int Y = (int)(0.2126 * r + 0.7152 * g + 0.0722 * b);

        // # Everything's shifted into place from the top two
        // # bits' original position - that is, bits 7-8.
        std::size_t packed;
        packed = (Y & top_two_bits) << 4;
        packed = packed | ((h & top_two_bits) << 2);
        packed = packed | ((l & top_two_bits) << 0);
        packed *= 4;

        samples[packed]     += r;
        samples[packed + 1] += g;
        samples[packed + 2] += b;
        samples[packed + 3] += 1;
    }

    return samples;
}

std::vector<std::tuple<long, std::size_t>> pick_used(std::vector<long>& samples){
    std::vector<std::tuple<long, std::size_t>> used;
    int count;
    for(std::size_t i=0; i<samples.size(); i+=4){
        count = samples[i + 3];
        if(count>0){
            used.push_back({count, i});
        }
    }
    return used;
}


std::vector<std::tuple<color_t, float>> get_colors(std::vector<long>& samples, std::vector<std::tuple<long, std::size_t>>& used, size_t number_of_colors){
    long pixels = 0;
    std::vector<std::tuple<color_t, float>> colors;
    number_of_colors = std::min(number_of_colors, used.size());

    long count;
    std::size_t index;
    for(size_t i=0; i<number_of_colors; i++){
        std::tie(count, index) = used[i];
        pixels += count;
        colors.push_back({{samples[index]/count, samples[index+1]/count, samples[index+2]/count}, (float)count});
    }

    for(int i=0; i<colors.size(); i++){
        std::get<1>(colors[i]) /= pixels;
    }
    return colors;
}


std::vector<std::tuple<color_t, float>> get_palette(py::array_t<uint8_t,  py::array::c_style> image, int color_count) {

    py::buffer_info image_buffer = image.request();

    if (image_buffer.ndim != 3) throw std::runtime_error("Image must be 3D matrix (height x width x color)");
    if (image_buffer.shape[2] != 3) throw std::runtime_error("Image must have 3 channels (red x green x blue)");

    std::vector<color_t> pixels;

    uint8_t* data = (uint8_t*)image_buffer.ptr;

    for (int pixel_index=0; pixel_index < image_buffer.shape[0] * image_buffer.shape[1]; pixel_index++) {
        pixels.push_back({data[pixel_index * 3], data[pixel_index * 3 + 1], data[pixel_index * 3 + 2]});
    }
    
    std::vector<long> samples;
    samples = sample(pixels);

    std::vector<std::tuple<long, std::size_t>> used;
    used = pick_used(samples);
    sort(used.begin(),used.end(),
       [](const std::tuple<long, std::size_t>& a,
       const std::tuple<long, std::size_t>& b) -> bool
       {
         return std::get<0>(a) > std::get<0>(b);
    });

    return get_colors(samples, used, color_count);
}


PYBIND11_MODULE(domicolor_backend, m) {
    m.def("get_palette", &get_palette, "Return color palette");
};