<?php

//debugging 
error_reporting(E_ALL);
ini_set('display_errors', '1');

class File {

//false if not found
//line if found
//returns first line
    static function SearchLine($filename, $search, $before, $exactMatch = false) {
        $lines = file($filename, FILE_IGNORE_NEW_LINES);
        foreach ($lines as $line) {
            $searchText = $line;
            if ($before !== null) {
                $split = explode($before, $line);
                $searchText = $split[0];
            }
            $trueOrNot = $exactMatch ? $searchText === $search : strpos($searchText, $search);
            if ($trueOrNot !== false) {
                return $line;
            }
        }
        return false;
    }

    static function AppendNewLineToFile($filename, $line) {
        file_put_contents($filename, "\n$line", FILE_APPEND);
    }

    static function RemoveLineMeetsCriteria($filename, $callbackOrNeedle) {
        $lines = file($filename, FILE_IGNORE_NEW_LINES);
        if (is_a($callbackOrNeedle, 'Callback')) {
            foreach ($lines as $key => $line) {
                if ($callbackOrNeedle->callback($line)) {
                    unset($lines[$key]);
                }
            }
        } else {
            foreach ($lines as $key => $line) {
                if (stristr($line, $callbackOrNeedle)) {
                    unset($lines[$key]);
                }
            }
        }


        $data = implode("\n", array_values($lines));

        $file = fopen($filename, 'w');
        fwrite($file, $data);
        fclose($file);
    }

    static function EditLine($filename, Callback $callback, $stopAtFirst = false) {
        $lines = file($filename, FILE_IGNORE_NEW_LINES);

        foreach ($lines as $key => $line) {
            $ret = $callback->callback($line);
            if ($ret !== null) {
                $lines[$key] = $ret;
                if ($stopAtFirst) {
                    break;
                }
            }
        }
        $data = implode("\n", array_values($lines));

        $file = fopen($filename, 'w');
        fwrite($file, $data);
        fclose($file);
    }

    static function LinesExcludeEmptyAsArray($filename) {
        $lines = file($filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        return $lines;
    }

    static function DeleteDir($dir) {
        if (substr($dir, strlen($dir) - 1, 1) != '/') {
            $dir .= '/';
        }
        if ($handle = opendir($dir)) {
            while ($obj = readdir($handle)) {
                if ($obj != '.' && $obj != '..') {
                    if (is_dir($dir . $obj)) {
                        if (!self::DeleteDir($dir . $obj))
                            return false;
                    }
                    elseif (is_file($dir . $obj)) {
                        if (!unlink($dir . $obj))
                            return false;
                    }
                }
            }

            closedir($handle);

            if (!@rmdir($dir))
                return false;
            return true;
        }
        return false;
    }

}

class URI {

    static function QUERY_GET($paramName, $default = null) {
        return isset($_GET[$paramName]) ? $_GET[$paramName] : $default;
    }

    static function QUERY_POST($paramName, $default = null) {
        return isset($_POST[$paramName]) ? $_POST[$paramName] : $default;
    }

    static function QUERY_ANY($paramName, $default = null) {
        return ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET[$paramName])) ? $_GET[$paramName] : (( $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST[$paramName])) ? $_POST[$paramName] : $default);
    }

    public static function HTTP_HOST() {
        return $_SERVER['HTTP_HOST'];
    }

    public static function HTTP_SELF() {
        return $_SERVER["PHP_SELF"];
    }

    public static function HTTP_SELF_DIR() {
        return dirname(self::HTTP_SELF());
    }

    public static function ADD_PARAM_TO_URL_STRING($url, $param) {
        $query = parse_url($url, PHP_URL_QUERY);
// Returns a string if the URL has parameters or NULL if not
        if ($query) {
            $url .= "&$param";
        } else {
            $url .= "&$param";
        }
        return $url;
    }

}

class SESSION {
    /*
     * @return bool
     */

    static function SESSION_IS_ACTIVE() {
        if (version_compare(phpversion(), '5.4.0', '>=')) {
            /*
              For >=PHP5.4
             */
            return session_status() === PHP_SESSION_ACTIVE;
        } if (version_compare(phpversion(), '5.3.0', '>=')) {
            /* http://stackoverflow.com/questions/3788369/how-to-tell-if-a-session-is-active/7656468#7656468
              For >=PHP5.3 && >=PHP5.4
             */
            $setting = 'session.use_trans_sid';
            $current = ini_get($setting);
            if (FALSE === $current) {
                throw new UnexpectedValueException(sprintf('Setting %s does not exists.', $setting));
            }
            $result = @ini_set($setting, $current);
            return $result !== $current;
        } else {
            /* http://stackoverflow.com/questions/3788369/how-to-tell-if-a-session-is-active/7656468#7656468
              For >=PHP5.2
             */
            $setting = 'session.use_trans_sid';
            $current = ini_get($setting);
            if (FALSE === $current) {
                throw new UnexpectedValueException(sprintf('Setting %s does not exists.', $setting));
            }
            $testate = "mix$current$current";
            $old = @ini_set($setting, $testate);
            $peek = @ini_set($setting, $current);
            $result = $peek === $current || $peek === FALSE;
            return $result;
        }
    }

}

interface Callback {

    function callback($args);
}
