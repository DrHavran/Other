import java.util.ArrayList;
import java.util.Arrays;
import java.util.regex.Pattern;

public class Main {
    public static void main(String[] args) {
        ArrayList<String> images = new ArrayList<>(Arrays.asList(
                "ALUNA 10 - Szafa 2d_1A0001",
                "ALUNA 10 - Szafa 2d_1B0001",
                "ALUNA 10 - Szafa 2d_1C0001",
                "ALUNA 10 - Szafa 2d_BIALE_1C0001",
                "ALUNA 10 - Szafa 2d_PB0010 Biały_1A0001",
                "ALUNA 10 - Szafa 2d_PB0010 Biały_1B0001",
                "ALUNA 10 - Szafa 2d_PU1001 Czarny Onyx_1A0001",
                "ALUNA 10 - Szafa 2d_PU1001 Czarny Onyx_1C0001",
                "ALUNA 11 - Szafa 2d_PB0010 Biały_1A0001",
                "ALUNA 13 - Szafa 3d_1C0001",
                "ALUNA 13 - Szafa 3d_BIALE_1C0001",
                "ALUNA 13 - Szafa 3d_PU1001 Czarny Onyx_1C0001",
                "aranz ALUNA 11 - Szafa 2d_PB0010 BIEL GORSKA_1A0001",
                "aranz ALUNA 11 - Szafa 2d_PU1001 Czarny Onyx_1A 0001",
                "aranz ALUNA 13_szafa 3D_1A0001",
                "aranz ALUNA 13_szafa 3D_PB0010 BIEL GORSKA_1A0001",
                "aranz ALUNA 13_szafa 3D_PU1001 Czarny Onyx_1A 0001",
                "aranz ALUNA 16 - Szafa 2d_PU1001 Czarny Onyx_1A 0001"
        ));

        ArrayList<String> names = new ArrayList<>(Arrays.asList(
                "ALUNA III 10 (150) PB0010-BIAŁY LAMINAT PB0010-BIAŁY LAMINAT 10III FSC B",
                "ALUNA III 10 (150) PD3016-DĄB ARTISAN PD3016-DĄB ARTISAN 10III FSC B",
                "ALUNA III 10 (150) PU1001-Czarny Onyx SG PU1001-Czarny Onyx SG 10III FSC B",
                "ALUNA III 11 (200) PB0010-BIAŁY LAMINAT PB0010-BIAŁY LAMINAT 11III FSC B",
                "ALUNA III 11 (200) PD3016-DĄB ARTISAN PD3016-DĄB ARTISAN 11III FSC B",
                "ALUNA III 11 (200) PU1001-Czarny Onyx SG PU1001-Czarny Onyx SG 11III FSC B",
                "ALUNA III 13 PB0010-BIAŁY LAMINAT PB0010-BIAŁY LAMINAT 13III FSC B",
                "ALUNA III 13 PD3016-DĄB ARTISAN PD3016-DĄB ARTISAN 13III FSC B",
                "ALUNA III 13 PU1001-Czarny Onyx SG PU1001-Czarny Onyx SG 13III FSC B",
                "ALUNA III 16 (120) PB0010-BIAŁY LAMINAT PB0010-BIAŁY LAMINAT 16III FSC B",
                "ALUNA III 16 (120) PD3016-DĄB ARTISAN PD3016-DĄB ARTISAN 16III FSC B",
                "ALUNA III 16 (120) PU1001-Czarny Onyx SG PU1001-Czarny Onyx SG 16III FSC B"
        ));


        for(String name : names){
            ArrayList<Integer> counts = new ArrayList<>();
            String[] parts = normalize(name).split("[ -]");
            for(String image : images){
                int count = 0;
                for(String part : parts){
                    try{
                        Integer.parseInt(part);
                        if (normalize(image).matches(".*(?<![a-zA-Z0-9])" + Pattern.quote(part) + "(?![a-zA-Z0-9]).*")) {
                            count += 32;
                        }
                    }
                    catch(NumberFormatException e){
                        if (normalize(image).contains(part)){
                            count ++;
                        }
                    }
                }
                counts.add(count);
            }
            int total = 0;
            for (int i : counts){
                total += i;
            }
            int average = (int) Math.ceil((double) total / counts.size()) + 1;
            System.out.print(name + " || ");
            for (int i = 0; i < counts.size(); i++) {
                if(counts.get(i) > average){
                    System.out.print(images.get(i) + " / ");
                }
            }
            System.out.println();
        }
    }
    private static String normalize(String s) {
        String norm = s.toLowerCase();
        norm = norm.replace("ł", "l")
                .replace("ą", "a")
                .replace("ć", "c")
                .replace("ę", "e")
                .replace("ń", "n")
                .replace("ó", "o")
                .replace("ś", "s")
                .replace("ź", "z")
                .replace("ż", "z");
        return norm;
    }
}