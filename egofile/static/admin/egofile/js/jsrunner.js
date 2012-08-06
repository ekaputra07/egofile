/* Ego JS Function Executer
 * Build and Run Javascript function based on returned data by File Browser 
 * @Author : Eka Putra - Egomedia Bali
 */
function egofile_do_actions(func_name, field_id, data){
    var Func = func_name+"('"+field_id+"','"+data+"')";
    eval(Func);
}
